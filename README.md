# متجر الجملة - الغردقة

## الملفات
- `index.html` : صفحة المتجر.
- `data/config.json` : اسم المتجر، رقم الواتساب (بصيغة 201XXXXXXXXX)، الحد الأدنى للطلب، وإظهار الأسعار (`showPrices`).
- `data/products.json` : المنتجات (يتولد من السكربت).
- `data/brands.json` : قواعد التعرف على الشركات من اسم المنتج.
- `data/unbranded_review.csv` : المنتجات اللي ملهاش شركة واضحة، للمراجعة.
- `logo.png` : اللوجو.
- `data/image_rules.json` : قواعد ربط الصور بالمنتجات حسب الاسم (صورة واحدة لعدة منتجات).
- `images/` : صور المنتجات وصور البانر (`banner-*.jpg`). سمّي الصورة بكود المنتج (SKU) مثل `6224008575993.jpg` وتتربط تلقائيًا.
- `tools/build_products.py` : يحدّث المنتجات من ملف CSV.

## تحديث المنتجات
    python tools/build_products.py ملف_المنتجات.csv
أضف `--include-unbranded` لو عايز المنتجات اللي ملهاش شركة تظهر تحت "أخرى".

## الرفع على GitHub
1. أنشئ Repository جديد (Public) وارفع كل الملفات.
2. Settings ← Pages ← اختر الفرع `main` والمجلد `/ (root)` ← Save.
3. بعد دقيقة أو اتنين الموقع يشتغل على `username.github.io/repo-name`.
