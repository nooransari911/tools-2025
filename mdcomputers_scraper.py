#!/usr/bin/env python3
"""Search & scrape product listings from MDComputers.in."""

import csv
import json
import sys
import time
from dataclasses import dataclass, asdict
from typing import Optional

import requests
from bs4 import BeautifulSoup

from ui import Colors, header, subheader, success, failure, print_kv, Table

BASE = "https://mdcomputers.in"
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

@dataclass
class Product:
    name: str
    price: str
    original_price: Optional[str]
    discount: Optional[str]
    product_url: str
    image_url: Optional[str]

def fetch(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": AGENT}, timeout=30)
    resp.raise_for_status()
    return resp.text

def extract(html: str) -> list[Product]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for wrapper in soup.select(".product-wrapper"):
        a = wrapper.select_one(".product-entities-title a")
        if not a:
            continue
        name = a.get_text(strip=True)
        url = a["href"].strip()
        if not url.startswith("http"):
            url = BASE + url
        img = wrapper.select_one(".product-element-top img")
        img_url = img["src"].strip() if img and img.get("src") else None
        price_el = wrapper.select_one(".price")
        orig = disc = None
        curr = ""
        if price_el:
            d = price_el.select_one(".del .amount")
            orig = d.get_text(strip=True) if d else None
            ins = price_el.select_one(".ins .amount")
            curr = ins.get_text(strip=True) if ins else price_el.get_text(strip=True)
        label = wrapper.select_one(".product-label")
        if label:
            disc = label.get_text(strip=True)
        out.append(Product(name, curr, orig, disc, url, img_url))
    return out

def total_pages(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    pag = soup.select_one(".pagination")
    if not pag:
        return 1
    nums = []
    for a in pag.find_all("a"):
        try:
            nums.append(int(a.get_text(strip=True)))
        except ValueError:
            continue
    return max(nums) if nums else 1

def search(query: str, max_pages: Optional[int] = None, delay: float = 1.0) -> list[Product]:
    all_prods = []
    first = fetch(f"{BASE}/?route=product/search&search={query}")
    all_prods.extend(extract(first))
    total = total_pages(first)
    pages = min(max_pages, total) if max_pages else total
    for page in range(2, pages + 1):
        time.sleep(delay)
        html = fetch(f"{BASE}/?route=product/search&search={query}&page={page}")
        all_prods.extend(extract(html))
    return all_prods

def render_table(products: list[Product]):
    table = Table(["#", "Product Name", "Price", "Orig.", "Disc."], [4, 72, 12, 12, 8])
    for i, p in enumerate(products, 1):
        name = p.name[:70] + "…" if len(p.name) > 72 else p.name
        price = f"{Colors.GREEN}{p.price}{Colors.END}" if p.discount else p.price
        table.add_row([str(i), name, price, p.original_price or "—", p.discount or "—"])
    table.render()

def export_json(products: list[Product]) -> str:
    return json.dumps([asdict(p) for p in products], indent=2, ensure_ascii=False)

def export_csv(products: list[Product]) -> str:
    buf = []
    writer = csv.writer(buf)
    writer.writerow(["name", "price", "original_price", "discount", "product_url", "image_url"])
    for p in products:
        writer.writerow([p.name, p.price, p.original_price, p.discount, p.product_url, p.image_url])
    return "".join(buf)

def main():
    header("MDComputers Product Search")

    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input(f"{Colors.BOLD}{Colors.CYAN}➤ Search term{Colors.END}: ").strip()
    if not query:
        failure("No search term provided.")
        sys.exit(1)

    subheader(f"Searching for \"{query}\"")
    try:
        products = search(query)
    except requests.RequestException as e:
        failure(f"Request failed: {e}")
        sys.exit(1)

    if not products:
        failure("No products found.")
        sys.exit(1)

    success(f"Found {len(products)} product{'s' if len(products) != 1 else ''}")
    print()
    render_table(products)

    try:
        choice = input(f"\n{Colors.BOLD}Save to file? (csv/json/— skip) [{Colors.GREEN}csv{Colors.END}{Colors.BOLD}]: {Colors.END}").strip().lower()
    except (EOFError, KeyboardInterrupt):
        choice = ""
    if choice not in ("csv", "json"):
        success("Done.")
        return

    filename = f"mdcomputers_{query.replace(' ', '_')}.{choice}"
    data = export_csv(products) if choice == "csv" else export_json(products)
    with open(filename, "w") as f:
        f.write(data)
    success(f"Saved {len(products)} products to {filename}")

if __name__ == "__main__":
    main()
