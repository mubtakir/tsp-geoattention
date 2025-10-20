# 🚀 البدء السريع

## التثبيت (30 ثانية)

```bash
cd tsp_geoattention
pip install -r requirements.txt
```

## التشغيل (اختر واحد)

### 1️⃣ الواجهة التفاعلية
```bash
streamlit run app.py
```
ثم افتح: `http://localhost:8501`

### 2️⃣ الاستخدام البرمجي
```python
from tsp_solver import TSPGeoAttention
import numpy as np

cities = [(np.random.rand() * 100, np.random.rand() * 100) 
          for _ in range(10)]
solver = TSPGeoAttention(cities, grid_size=3)
tour = solver.solve()
print(f"المسار: {tour}")
print(f"المسافة: {solver.get_tour_distance(tour):.2f}")
```

### 3️⃣ الأمثلة
```bash
python example_usage.py
```

### 4️⃣ الاختبارات
```bash
pytest test_tsp_solver.py -v
```

## 📚 المزيد من المعلومات

- [README](README.md) - الملخص الشامل
- [ALGORITHM.md](ALGORITHM.md) - شرح الخوارزمية
- [FAQ.md](FAQ.md) - الأسئلة الشائعة
- [INSTALLATION.md](INSTALLATION.md) - دليل التثبيت المفصل

## ⚡ نصائح سريعة

- **grid_size**: 2-3 للمشاكل الصغيرة، 5-8 للكبيرة
- **distance_type**: 'euclidean' للمشاكل التجريدية، 'haversine' للمدن الحقيقية
- **max_iterations**: زيادتها تحسّن النتائج لكن تبطّئ الحل

## 🎯 مثال سريع

```python
from tsp_solver import TSPGeoAttention

# 4 مدن في مربع
cities = [(0, 0), (1, 0), (1, 1), (0, 1)]

# حل المسألة
solver = TSPGeoAttention(cities, grid_size=2)
tour = solver.solve()

# النتيجة
print(tour)  # [0, 1, 2, 3] أو ترتيب مشابه
```

---

**استمتع بالحل! 🎉**
