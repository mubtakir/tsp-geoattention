"""
TSP-GeoAttention Interactive Application
=========================================
واجهة تفاعلية لحل مسألة البائع المتجول
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from tsp_solver import (
    TSPGeoAttention, compute_tour_distance, solve_tsp_exact, 
    read_tsplib, euclidean_distance
)
import tempfile
import os
import pandas as pd
from io import BytesIO

# ==================== إعداد الصفحة ====================

st.set_page_config(
    page_title="TSP-GeoAttention Solver",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS مخصص
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF4B4B;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1em;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🗺️ TSP-GeoAttention Solver</div>', unsafe_allow_html=True)
st.markdown("""
<div class="subtitle">
حل هجين مبتكر لمسألة البائع المتجول باستخدام الهندسة المكانية والانتباه الديناميكي
</div>
""", unsafe_allow_html=True)

# ==================== الشريط الجانبي ====================

st.sidebar.header("⚙️ الإعدادات")

# اختيار مصدر البيانات
data_source = st.sidebar.radio(
    "📊 اختر مصدر المدن:",
    ("🎲 بيانات عشوائية", "📂 تحميل ملف TSPLIB", "✏️ رسم يدوي")
)

cities = []

# ==================== معالجة مصادر البيانات ====================

if data_source == "🎲 بيانات عشوائية":
    num_cities = st.sidebar.slider("عدد المدن", 3, 20, 8)
    seed = st.sidebar.number_input("Seed", value=42, min_value=0)
    np.random.seed(int(seed))
    cities = [(np.random.rand() * 100, np.random.rand() * 100) for _ in range(num_cities)]
    st.sidebar.success(f"✅ تم توليد {num_cities} مدينة عشوائية")

elif data_source == "📂 تحميل ملف TSPLIB":
    uploaded_file = st.sidebar.file_uploader("اختر ملف .tsp", type=["tsp"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tsp") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        try:
            cities = read_tsplib(tmp_path)
            st.sidebar.success(f"✅ تم تحميل {len(cities)} مدينة!")
        except Exception as e:
            st.sidebar.error(f"❌ خطأ: {e}")
        finally:
            os.unlink(tmp_path)

else:  # رسم يدوي
    if 'drawn_cities' not in st.session_state:
        st.session_state.drawn_cities = []
    
    if st.sidebar.button("🗑️ مسح جميع المدن"):
        st.session_state.drawn_cities = []
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        x_input = st.number_input("X", min_value=0.0, max_value=100.0, value=50.0)
    with col2:
        y_input = st.number_input("Y", min_value=0.0, max_value=100.0, value=50.0)
    
    if st.sidebar.button("➕ إضافة مدينة") and len(st.session_state.drawn_cities) < 15:
        st.session_state.drawn_cities.append((x_input, y_input))
    
    cities = st.session_state.drawn_cities
    if cities:
        st.sidebar.info(f"📍 عدد المدن المرسومة: {len(cities)}")

# ==================== إعدادات الخوارزمية ====================

st.sidebar.markdown("---")
st.sidebar.header("🔧 إعدادات الخوارزمية")

distance_type = st.sidebar.selectbox(
    "نوع المسافة",
    ["إقليدية (2D)", "جوية (Great-circle)"]
)
dist_type = 'haversine' if 'جوية' in distance_type else 'euclidean'

if cities:
    n = len(cities)
    grid_size = st.sidebar.slider(
        "حجم الشبكة (Grid Size)", 
        2, 8, 
        min(5, max(3, n//2))
    )
    
    max_iterations = st.sidebar.slider(
        "عدد تكرارات التحسين (2-opt)",
        50, 500, 200
    )

# ==================== المحتوى الرئيسي ====================

if cities:
    n = len(cities)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📍 عدد المدن", n)
    with col2:
        st.metric("📏 نوع المسافة", "إقليدية" if dist_type == 'euclidean' else "جوية")
    with col3:
        st.metric("🔲 حجم الشبكة", f"{grid_size}×{grid_size}")
    
    st.markdown("---")
    
    # زر الحل
    if st.button("🚀 حل المسألة", key="solve_button", use_container_width=True):
        with st.spinner("⏳ جاري الحساب..."):
            # الحل التقريبي
            solver = TSPGeoAttention(cities, grid_size=grid_size, distance_type=dist_type)
            approx_tour = solver.solve()
            approx_dist = solver.get_tour_distance(approx_tour)
            
            # الحل الأمثل (إن أمكن)
            exact_tour, exact_dist = None, None
            error_pct = None
            if n <= 10:
                exact_tour, exact_dist = solve_tsp_exact(np.array(cities))
                if exact_tour is not None:
                    error_pct = 100 * (approx_dist - exact_dist) / exact_dist
            
            # عرض النتائج
            st.success("✅ تم حل المسألة بنجاح!")
            
            result_col1, result_col2, result_col3 = st.columns(3)
            with result_col1:
                st.metric("المسافة التقريبية", f"{approx_dist:.2f}")
            with result_col2:
                if error_pct is not None:
                    st.metric("نسبة الخطأ", f"{error_pct:.2f}%", 
                             delta=f"من الأمثل" if error_pct >= 0 else "أفضل من المتوقع")
                else:
                    st.metric("الحل الأمثل", "غير محسوب (n > 10)")
            with result_col3:
                if exact_dist is not None:
                    st.metric("المسافة الأمثلية", f"{exact_dist:.2f}")
            
            # الرسوم البيانية
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # الرسم التقريبي
            xs, ys = zip(*cities)
            axes[0].scatter(xs, ys, c='blue', s=100, zorder=5, edgecolors='black', linewidth=1.5)
            tour_points = [cities[i] for i in approx_tour] + [cities[approx_tour[0]]]
            tx, ty = zip(*tour_points)
            axes[0].plot(tx, ty, 'r--', linewidth=2, alpha=0.8, label='المسار')
            axes[0].set_title(f"الحل التقريبي\nالمسافة = {approx_dist:.1f}", fontsize=12, fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            axes[0].legend()
            
            # الرسم الأمثل أو المقارنة
            if exact_tour is not None:
                axes[1].scatter(xs, ys, c='green', s=100, zorder=5, edgecolors='black', linewidth=1.5)
                tour_opt = [cities[i] for i in exact_tour] + [cities[exact_tour[0]]]
                tx_opt, ty_opt = zip(*tour_opt)
                axes[1].plot(tx_opt, ty_opt, 'g-', linewidth=2.5, alpha=0.9, label='المسار الأمثل')
                axes[1].set_title(f"الحل الأمثلي\nالمسافة = {exact_dist:.1f}", fontsize=12, fontweight='bold')
                axes[1].legend()
            else:
                axes[1].scatter(xs, ys, c='blue', s=100, zorder=5, edgecolors='black', linewidth=1.5)
                axes[1].plot(tx, ty, 'r--', linewidth=2, alpha=0.8)
                axes[1].set_title("الحل التقريبي (لا يوجد حل أمثل للمقارنة)", fontsize=12, fontweight='bold')
            
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # عرض المسار
            st.subheader("📋 تفاصيل المسار")
            path_str = " → ".join(map(str, approx_tour)) + " → " + str(approx_tour[0])
            st.code(path_str, language="text")
            
            # تصدير النتائج
            st.subheader("💾 تصدير النتائج")
            
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                # تصدير CSV
                tour_df = pd.DataFrame({
                    'ترتيب': range(len(approx_tour)),
                    'فهرس_المدينة': approx_tour,
                    'X': [cities[i][0] for i in approx_tour],
                    'Y': [cities[i][1] for i in approx_tour]
                })
                csv = tour_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    "📥 تحميل المسار (CSV)",
                    csv,
                    "tsp_solution.csv",
                    "text/csv"
                )
            
            with col_export2:
                # تصدير الصورة
                img_buffer = BytesIO()
                fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
                img_buffer.seek(0)
                st.download_button(
                    "🖼️ تحميل الصورة (PNG)",
                    img_buffer,
                    "tsp_solution.png",
                    "image/png"
                )

else:
    st.info("👈 يرجى إضافة مدن عبر الشريط الجانبي لبدء الحل")

# ==================== معلومات إضافية ====================

st.markdown("---")
st.markdown("""
### 📚 عن هذا الحل

هذا النهج الهجين يجمع بين ثلاثة مفاهيم أساسية:

1. **🏙️ الهندسة المكانية**: تقسيم المدينة إلى أحياء (خلايا) لتقليل فضاء البحث
2. **⚛️ مبدأ الفعل الأدنى**: اختيار المسار ذو التكلفة الأدنى (من الفيزياء الكلاسيكية)
3. **🧠 آلية الانتباه**: استخدام softmax لاختيار أفضل الانتقالات (من نماذج الترانسفورمر)

**الباحث**: باسل يحيى عبدالله
""")

st.caption("⚠️ ملاحظة: هذا حل تقريبي ولا يضمن الأمثلية، لكنه فعّال عمليًا للمشاكل الكبيرة")

