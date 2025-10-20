# 📦 دليل التثبيت الشامل

## المتطلبات الأساسية

- **Python**: 3.8 أو أحدث
- **pip**: مدير الحزم
- **git**: للاستنساخ (اختياري)

## التثبيت السريع

### 1. استنساخ المستودع

```bash
git clone https://github.com/your-username/tsp-geoattention.git
cd tsp-geoattention
```

أو تحميل الملفات مباشرة من GitHub.

### 2. إنشاء بيئة افتراضية (موصى به)

```bash
# على Linux/Mac
python3 -m venv venv
source venv/bin/activate

# على Windows
python -m venv venv
venv\Scripts\activate
```

### 3. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 4. التحقق من التثبيت

```bash
python -c "from tsp_solver import TSPGeoAttention; print('✅ التثبيت نجح!')"
```

---

## التثبيت المتقدم

### تثبيت مع أدوات التطوير

```bash
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy
```

### تثبيت من المصدر

```bash
git clone https://github.com/your-username/tsp-geoattention.git
cd tsp-geoattention
pip install -e .
```

---

## تشغيل التطبيق

### الواجهة التفاعلية (Streamlit)

```bash
streamlit run app.py
```

سيفتح المتصفح على: `http://localhost:8501`

### الاستخدام البرمجي

```python
from tsp_solver import TSPGeoAttention
import numpy as np

# إنشاء مدن عشوائية
cities = [(np.random.rand() * 100, np.random.rand() * 100) 
          for _ in range(10)]

# حل المسألة
solver = TSPGeoAttention(cities, grid_size=3)
tour = solver.solve()
distance = solver.get_tour_distance(tour)

print(f"المسار: {tour}")
print(f"المسافة: {distance:.2f}")
```

### تشغيل الأمثلة

```bash
python example_usage.py
```

---

## تشغيل الاختبارات

### جميع الاختبارات

```bash
pytest test_tsp_solver.py -v
```

### مع تقرير التغطية

```bash
pytest test_tsp_solver.py -v --cov=tsp_solver --cov-report=html
```

### اختبار محدد

```bash
pytest test_tsp_solver.py::TestTSPGeoAttention::test_solve_returns_valid_tour -v
```

---

## استكشاف الأخطاء

### خطأ: `ModuleNotFoundError: No module named 'streamlit'`

```bash
pip install streamlit
```

### خطأ: `ModuleNotFoundError: No module named 'numpy'`

```bash
pip install numpy
```

### خطأ: `Permission denied` على Linux/Mac

```bash
chmod +x app.py
```

### البيئة الافتراضية لا تعمل

```bash
# حذف البيئة القديمة
rm -rf venv

# إنشاء جديدة
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## التثبيت على أنظمة مختلفة

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv
git clone https://github.com/your-username/tsp-geoattention.git
cd tsp-geoattention
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### macOS

```bash
brew install python3
git clone https://github.com/your-username/tsp-geoattention.git
cd tsp-geoattention
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
# تحميل Python من python.org
git clone https://github.com/your-username/tsp-geoattention.git
cd tsp-geoattention
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## النشر على Streamlit Cloud

### الخطوات

1. أنشئ حسابًا على [Streamlit Cloud](https://streamlit.io/cloud)
2. ربط حسابك بـ GitHub
3. اختر المستودع `tsp-geoattention`
4. اختر الفرع `main`
5. المسار الرئيسي: `app.py`
6. انقر **Deploy**

### المتطلبات

- ملف `requirements.txt` محدث
- ملف `app.py` في الجذر
- مستودع عام على GitHub

---

## الترقية

```bash
# ترقية جميع الحزم
pip install --upgrade -r requirements.txt

# ترقية حزمة محددة
pip install --upgrade streamlit
```

---

## إلغاء التثبيت

```bash
# إلغاء البيئة الافتراضية
rm -rf venv

# أو على Windows
rmdir /s venv
```

---

## الدعم

إذا واجهت مشاكل:
1. تحقق من [الأسئلة الشائعة](FAQ.md)
2. ابحث في [Issues](https://github.com/your-username/tsp-geoattention/issues)
3. أنشئ issue جديد مع التفاصيل

---

**آخر تحديث**: 2024

