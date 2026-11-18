#!/usr/bin/env python3
"""يحوّل ملف المنتجات (CSV) إلى data/products.json ويطبع تقرير بالمشاكل.
الاستخدام:  python tools/build_products.py ملف.csv [--include-unbranded]
الأعمدة المقبولة: تصدير WooCommerce (Name, Regular price, SKU, Short description, Categories)
أو ملف بسيط (name, price, sku, type, brand).
"""
import csv, json, re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPE_KEYS = [("سيرب","سيرب"),("صوص","صوص"),("صلصه","صوص"),("مايونيز","صوص"),("بن ","بن"),("قهوة","بن"),("قهوه","بن"),("اسبريسو","بن"),("نسكافيه","بن"),("عصير","عصائر"),("كراش","عصائر"),("بيوريه","عصائر"),("شاي","شاي"),("شوكولا","شوكولاته"),("شيكولا","شوكولاته"),("شكولا","شوكولاته"),("نوتيلا","شوكولاته"),("ايس كريم","آيس كريم"),("بودر","بودر"),("فرابيه","فرابيه"),("حليب","ألبان"),("كريمة","ألبان"),("مكنة","معدات"),("مطحنة","معدات"),("بسكوت","بسكوت"),("فلتر","مستلزمات"),("كوب","مستلزمات"),("بار مات","مستلزمات")]

def pick(r, *keys):
    for k in keys:
        if r.get(k) not in (None, ""): return r[k].strip()
    return ""

def brand_of(name, rules):
    low = name.lower()
    for b in rules:
        for k in b["keywords"]:
            if (k.startswith("re:") and re.search(k[3:], low)) or (not k.startswith("re:") and k.lower() in low):
                return b["name"]
    return None

IMG_RULES = []
def main():
    global IMG_RULES
    src = sys.argv[1]; keep_all = "--include-unbranded" in sys.argv
    rules = json.load(open(f"{ROOT}/data/brands.json", encoding="utf-8"))
    IMG_RULES = json.load(open(f"{ROOT}/data/image_rules.json", encoding="utf-8")) if os.path.exists(f"{ROOT}/data/image_rules.json") else []
    img_dir = f"{ROOT}/images"; seen, out, unbranded, issues = set(), [], [], []
    for r in csv.DictReader(open(src, encoding="utf-8-sig")):
        name = re.sub(r"\s+", " ", pick(r, "Name", "name")).strip()
        try: price = float(pick(r, "Regular price", "price") or 0)
        except ValueError: price = 0
        sku = pick(r, "SKU", "sku")
        if not name or name == "تست" or price <= 5: issues.append(f"تم تجاهل: {name!r} (سعر {price})"); continue
        key = (name, sku)
        if key in seen: issues.append(f"مكرر: {name}"); continue
        seen.add(key)
        brand = pick(r, "brand") or brand_of(name, rules)
        t = pick(r, "type") or next((v for k, v in TYPE_KEYS if k in name + " "), "")
        image = next((f"images/{sku}.{e}" for e in ("jpg","png","webp") if sku and os.path.exists(f"{img_dir}/{sku}.{e}")), "")
        image = image or next((r["image"] for r in IMG_RULES if all(k.lower() in name.lower() for k in r["all"]) and os.path.exists(f"{ROOT}/{r['image']}")), "")
        p = {"id": sku or f"p{len(out)+1}", "name": name, "brand": brand or "أخرى", "type": t, "price": price, "image": image}
        (out if (brand or keep_all) else unbranded).append(p)
    json.dump(out, open(f"{ROOT}/data/products.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if unbranded:
        with open(f"{ROOT}/data/unbranded_review.csv", "w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, ["id","name","type","price","brand"]); w.writeheader()
            for p in unbranded: w.writerow({k: p.get(k, "") for k in w.fieldnames})
    print(f"تم: {len(out)} منتج في products.json | بدون شركة واضحة: {len(unbranded)} (data/unbranded_review.csv)")
    print(f"صور مربوطة: {sum(1 for p in out if p['image'])}")
    for i in issues: print(" -", i)
main()
