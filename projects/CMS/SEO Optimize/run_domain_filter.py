import json
import os
import re
import sys
from openai import OpenAI
import pandas as pd

use_ai = '--no-ai' not in sys.argv

# 1. Parse API key
api_key = None
if use_ai:
    with open(os.path.expanduser('~/.secrets/secrets.txt'), 'r') as f:
        for line in f:
            if line.startswith('NEUROMETRIC_API_KEY='):
                api_key = line.strip().split('=', 1)[1]
                break

    if not api_key:
        raise ValueError("API key not found")

    # 2. Setup OpenAI client
    client = OpenAI(
        base_url="https://api.neurometric.ai/v1",
        api_key=api_key
    )

# 3. Load data and filter by TF != 0
data = json.load(open('data/raw/auctions_ending_today.json'))['data']

def parse_price(p):
    try:
        if isinstance(p, (int, float)): return float(p)
        if isinstance(p, str): return float(re.sub(r'[^\d.]', '', p))
        return float('inf')
    except:
        return float('inf')

for d in data:
    d['parsed_price'] = parse_price(d.get('price'))

# Filter valid prices, TF >= 5, and Backlinks / RD < 10
valid_data = []
for d in data:
    if d['parsed_price'] <= 1.0 or d['parsed_price'] == float('inf'):
        continue
    as_score = d.get('semrushAs', 0)
    bl = d.get('majesticBacklinks', 0)
    rd = d.get('majesticReferringDomains', 0)
    if as_score >= 5 and rd > 0 and (bl / rd) < 10:
        valid_data.append(d)

# Sort by cheapest first
valid_data.sort(key=lambda x: x['parsed_price'])

# Get top 400
top_400 = valid_data[:400]

# 4. Prepare batch for LLM
domain_list_str = "\n".join([f"{i}. {d['domainName']}" for i, d in enumerate(top_400)])

prompt = f"""
Here is a list of domain names. I need you to filter out the "spam" domains.
You should filter OUT ONLY literal rubbish or nonsensical domains:
1. Keyboard smash or obvious gibberish (e.g. jfksldjfksd.com)
2. Numbers-only domains (e.g. 1234567.com)
3. Highly unnatural, unpronounceable consonant combinations (e.g. xqzpwk.com)

You MUST KEEP (DO NOT filter out) everything else. If it is even plausibly a name, a brand, or a foreign word, keep it. 
Examples of things to KEEP:
- Legible English words
- Plausibly names (e.g. johnsmith.com, thanassiscambanis.com)
- Brandable or foreign words that are easily pronounceable (e.g. tacoderio.com)

Please return ONLY a JSON list of integers representing the index of the NON-SPAM domains. Do not include any other text or markdown formatting. Just the JSON array.
Example: [0, 2, 5, 12, 199]

Domain list:
{domain_list_str}
"""

if use_ai:
    print(f"Sending request to API for {len(top_400)} domains...")
    response = client.chat.completions.create(
        model="neurometric/clawpack",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content
    print("API Response:", reply)

    # 5. Parse response and dump results
    try:
        match = re.search(r'\[\s*\d.*?\]', reply, re.DOTALL)
        if match:
            indices = json.loads(match.group(0))
        else:
            indices = json.loads(reply)
    except Exception as e:
        print(f"Failed to parse API results: {e}")
        indices = []
else:
    print(f"AI disabled via --no-ai. Processing all {len(top_400)} domains...")
    indices = list(range(len(top_400)))

try:
    results = []
    for idx in indices:
        if 0 <= idx < len(top_400):
            d = top_400[idx]
            results.append({
                'Domain': d.get('domainName'),
                'Price': d.get('price'),
                'Semrush AS': d.get('semrushAs'),
                'Semrush Traffic': d.get('semrushSearchVolume'),
                'Backlinks': d.get('majesticBacklinks'),
                'Ref Domains': d.get('majesticReferringDomains')
            })
            
    df = pd.DataFrame(results)
    
    # Sort by Semrush AS (descending, since higher AS is better)
    if not df.empty:
        df['Semrush AS'] = pd.to_numeric(df['Semrush AS'], errors='coerce').fillna(0)
        df = df.sort_values(by='Semrush AS', ascending=False)
        
    df.to_csv('data/processed/premium_domains_filtered.csv', index=False)
    print(f"Saved {len(results)} non-spam domains to data/processed/premium_domains_filtered.csv")
    
except Exception as e:
    print(f"Failed to parse or save results: {e}")
