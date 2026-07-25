#!/usr/bin/env python3
"""Scrape product details from MDComputers.in for a given search term."""

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
BASE_URL = "https://mdcomputers.in"


@dataclass
class Product:
    name: str
    price: str
    original_price: Optional[str]
    discount: Optional[str]
    product_url: str
    image_url: Optional[str]


def parse_price(price_text: str) -> str:
    return price_text.replace("\u20b9", "₹").strip()


def extract_products(html: str) -> list[Product]:
    soup = BeautifulSoup(html, "html.parser")
    products: list[Product] = []

    for wrapper in soup.select(".product-wrapper"):
        name_el = wrapper.select_one(".product-entities-title a")
        if not name_el:
            continue
        name = name_el.get_text(strip=True)
        product_url = name_el.get("href", "").strip()
        if product_url and not product_url.startswith("http"):
            product_url = BASE_URL + product_url

        image_el = wrapper.select_one(".product-element-top img")
        image_url = image_el.get("src", "").strip() if image_el else None

        price_el = wrapper.select_one(".price")
        original_price = None
        discount = None
        current_price = ""

        if price_el:
            del_el = price_el.select_one(".del .amount")
            original_price = parse_price(del_el.get_text(strip=True)) if del_el else None
            ins_el = price_el.select_one(".ins .amount")
            current_price = parse_price(ins_el.get_text(strip=True)) if ins_el else price_el.get_text(strip=True)

        label_el = wrapper.select_one(".product-label")
        if label_el:
            discount = label_el.get_text(strip=True)

        products.append(Product(
            name=name,
            price=current_price,
            original_price=original_price,
            discount=discount,
            product_url=product_url,
            image_url=image_url,
        ))

    return products


def get_total_pages(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.select_one(".pagination")
    if not pagination:
        return 1
    links = pagination.find_all("a")
    max_page = 1
    for a in links:
        try:
            page_num = int(a.get_text(strip=True))
            if page_num > max_page:
                max_page = page_num
        except ValueError:
            continue
    return max_page


def search(
    query: str,
    max_pages: int = None,
    delay: float = 1.0,
) -> list[Product]:
    all_products: list[Product] = []
    session = requests.Session()
    session.headers.update(HEADERS)

    first_url = f"{BASE_URL}/?route=product/search&search={query}"
    resp = session.get(first_url, timeout=30)
    resp.raise_for_status()
    all_products.extend(extract_products(resp.text))
    total = get_total_pages(resp.text)

    if not max_pages or max_pages > total:
        max_pages = total

    for page in range(2, max_pages + 1):
        time.sleep(delay)
        url = f"{BASE_URL}/?route=product/search&search={query}&page={page}"
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        all_products.extend(extract_products(resp.text))

    return all_products


def print_table(products: list[Product]):
    fmt = "{:<5} {:<60} {:<15} {:<15} {:<10} {:<70}"
    print(fmt.format("#", "Name", "Price", "Orig Price", "Discount", "URL"))
    print("-" * 180)
    for i, p in enumerate(products, 1):
        name = p.name[:58] + ".." if len(p.name) > 60 else p.name
        print(fmt.format(
            i, name, p.price,
            p.original_price or "-",
            p.discount or "-",
            p.product_url,
        ))


def main():
    parser = argparse.ArgumentParser(description="Scrape MDComputers.in product search results")
    parser.add_argument("search", help="Search term (e.g. 'external harddrive')")
    parser.add_argument("--pages", type=int, default=None, help="Max pages to scrape (default: all)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between page requests in seconds (default: 1.0)")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format (default: table)")
    parser.add_argument("--output", "-o", help="Output file path (optional)")
    args = parser.parse_args()

    products = search(args.search, max_pages=args.pages, delay=args.delay)

    if not products:
        print("No products found.", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        data = json.dumps([asdict(p) for p in products], indent=2, ensure_ascii=False)
    elif args.format == "csv":
        import io
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["name", "price", "original_price", "discount", "product_url", "image_url"])
        writer.writeheader()
        for p in products:
            writer.writerow(asdict(p))
        data = buf.getvalue()
    else:
        print_table(products)
        return

    if args.output:
        with open(args.output, "w") as f:
            f.write(data)
        print(f"Saved {len(products)} products to {args.output}")
    else:
        print(data)


if __name__ == "__main__":
    main()
