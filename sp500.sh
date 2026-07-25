#!/usr/bin/env bash
set -euo pipefail

URL="${1:-https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv}"

script=$(mktemp)
trap 'rm -f "$script"' EXIT

cat > "$script" <<'PYEOF'
import csv, re, sys

data = sys.stdin.read()
lines = data.splitlines()
if not lines:
    print("Error: empty CSV", file=sys.stderr)
    sys.exit(1)

# Phase 1 — validate every line has the same field count as the header
# (handles quoted commas correctly by using csv.reader)
sample = csv.reader(lines)
header = next(sample, None)
if header is None:
    print("Error: no header row found", file=sys.stderr)
    sys.exit(1)

expected = len(header)
for lineno, row in enumerate(sample, 2):
    if len(row) != expected:
        print(
            f"Error: excess/missing comma on line {lineno} "
            f"(expected {expected} fields, got {len(row)})",
            file=sys.stderr,
        )
        sys.exit(1)

# Phase 2 — parse as dicts (now guaranteed consistent)
reader = csv.DictReader(lines)
fieldnames = reader.fieldnames

col_name = "Security"
col_loc  = "Headquarters Location"
col_year = "Founded"

missing = {col_name, col_loc, col_year} - set(fieldnames)
if missing:
    print(f"Error: columns not found: {', '.join(sorted(missing))}", file=sys.stderr)
    sys.exit(1)

rows = []
for row in reader:
    name = row[col_name].strip()
    loc  = row[col_loc].strip()
    raw  = row[col_year].strip()
    m = re.search(r'\b(\d{4})\b', raw)
    year = int(m.group(1)) if m else 0
    rows.append((year, name, loc))

rows.sort(key=lambda x: x[0])

print(f"{'Company':60} {'Location':42} {'Year'}")
print("-" * 112)
for year, name, loc in rows:
    print(f"{name:60} {loc:42} {year}")
PYEOF

curl -sL --fail "$URL" | python3 "$script"
