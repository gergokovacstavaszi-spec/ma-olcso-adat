import json
import sys
import urllib.request
from datetime import datetime, timezone
 
CATS = {
    "csirkemell": 18, "tojás": 14, "hagyma": 40, "paradicsom": 34,
    "tészta": 50, "burgonya": 41, "rizs": 95, "tejföl": 5,
    "sajt": 10, "kolbász": 88, "fokhagyma": 39, "sárgarépa": 36,
    "paprika": 35, "uborka": 38, "káposzta": 43, "brokkoli": 97,
    "tej": 3, "étolaj": 51, "liszt": 52, "vaj": 12,
    "darált sertés": 85, "darált marha": 86, "lencse": 96, "kenyér": 46,
    "kukorica": 56, "zöldborsó": 59, "szalonna": 89, "joghurt": 7, "túró": 9,
}
 
API = "https://arfigyelo.gvh.hu/api/products-by-category/"
 
def fetch_cheapest(category_id):
    url = API + str(category_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        data = json.load(r)
    best = None
    for p in data.get("products", []):
        price = p.get("minUnitPrice")
        if not price:
            continue
        if best is None or price < best["p"]:
            chain = (p.get("pricesOfChainStores") or [{}])[0].get("name", "")
            best = {"p": price, "chain": chain}
    return best
 
result = {}
for name, cat_id in CATS.items():
    try:
        result[name] = fetch_cheapest(cat_id)
        print(f"{name}: ok", file=sys.stderr)
    except Exception as e:
        print(f"{name}: failed ({e})", file=sys.stderr)
 
output = {
    "meta": {"updated": datetime.now(timezone.utc).isoformat()},
    "ingredients": result,
}
print(json.dumps(output, ensure_ascii=False))