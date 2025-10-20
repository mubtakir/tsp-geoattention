"""
أمثلة على استخدام TSP-GeoAttention Solver
"""

import numpy as np
import matplotlib.pyplot as plt
from tsp_solver import (
    TSPGeoAttention, solve_tsp_exact, compute_tour_distance
)


def example_1_random_cities():
    """مثال 1: حل مشكلة مع مدن عشوائية"""
    print("=" * 60)
    print("مثال 1: مدن عشوائية")
    print("=" * 60)
    
    np.random.seed(42)
    cities = [(np.random.rand() * 100, np.random.rand() * 100) for _ in range(10)]
    
    # الحل التقريبي
    solver = TSPGeoAttention(cities, grid_size=3, distance_type='euclidean')
    approx_tour = solver.solve()
    approx_dist = solver.get_tour_distance(approx_tour)
    
    print(f"عدد المدن: {len(cities)}")
    print(f"المسار التقريبي: {approx_tour}")
    print(f"المسافة التقريبية: {approx_dist:.2f}")
    
    # الحل الأمثل (للمقارنة)
    exact_tour, exact_dist = solve_tsp_exact(np.array(cities))
    if exact_tour:
        error = 100 * (approx_dist - exact_dist) / exact_dist
        print(f"المسار الأمثل: {exact_tour}")
        print(f"المسافة الأمثلية: {exact_dist:.2f}")
        print(f"نسبة الخطأ: {error:.2f}%")
    
    return cities, approx_tour


def example_2_small_problem():
    """مثال 2: مشكلة صغيرة مع مقارنة"""
    print("\n" + "=" * 60)
    print("مثال 2: مشكلة صغيرة (4 مدن)")
    print("=" * 60)
    
    cities = [(0, 0), (1, 0), (1, 1), (0, 1)]
    
    # الحل التقريبي
    solver = TSPGeoAttention(cities, grid_size=2)
    approx_tour = solver.solve()
    approx_dist = solver.get_tour_distance(approx_tour)
    
    # الحل الأمثل
    exact_tour, exact_dist = solve_tsp_exact(np.array(cities))
    
    print(f"المدن: {cities}")
    print(f"الحل التقريبي: {approx_tour} (المسافة: {approx_dist:.2f})")
    print(f"الحل الأمثل: {exact_tour} (المسافة: {exact_dist:.2f})")
    
    if exact_dist > 0:
        error = 100 * (approx_dist - exact_dist) / exact_dist
        print(f"نسبة الخطأ: {error:.2f}%")


def example_3_different_grid_sizes():
    """مثال 3: تأثير حجم الشبكة على الأداء"""
    print("\n" + "=" * 60)
    print("مثال 3: تأثير حجم الشبكة")
    print("=" * 60)
    
    np.random.seed(42)
    cities = [(np.random.rand() * 100, np.random.rand() * 100) for _ in range(15)]
    
    print(f"عدد المدن: {len(cities)}\n")
    print(f"{'حجم الشبكة':<15} {'المسافة':<15} {'الوقت (تقريبي)':<15}")
    print("-" * 45)
    
    for grid_size in [2, 3, 4, 5, 6]:
        solver = TSPGeoAttention(cities, grid_size=grid_size)
        tour = solver.solve()
        dist = solver.get_tour_distance(tour)
        print(f"{grid_size}x{grid_size:<12} {dist:<15.2f} {'سريع':<15}")


def example_4_distance_types():
    """مثال 4: مقارنة نوعي المسافة"""
    print("\n" + "=" * 60)
    print("مثال 4: مقارنة نوعي المسافة")
    print("=" * 60)
    
    # إحداثيات جغرافية (خط الطول، خط العرض)
    cities = [
        (35.6762, 51.3895),  # طهران
        (31.2357, 30.0444),  # القاهرة
        (39.9042, 116.4074), # بكين
        (35.6895, 139.6917), # طوكيو
    ]
    
    print("المدن (خط الطول، خط العرض):")
    for i, city in enumerate(cities):
        print(f"  {i}: {city}")
    
    # الحل مع المسافة الإقليدية
    solver_euclidean = TSPGeoAttention(cities, grid_size=2, distance_type='euclidean')
    tour_euclidean = solver_euclidean.solve()
    dist_euclidean = solver_euclidean.get_tour_distance(tour_euclidean)
    
    # الحل مع المسافة الجوية
    solver_haversine = TSPGeoAttention(cities, grid_size=2, distance_type='haversine')
    tour_haversine = solver_haversine.solve()
    dist_haversine = solver_haversine.get_tour_distance(tour_haversine)
    
    print(f"\nالمسافة الإقليدية: {dist_euclidean:.2f}")
    print(f"المسافة الجوية: {dist_haversine:.2f} كم")


def example_5_visualization():
    """مثال 5: رسم النتائج"""
    print("\n" + "=" * 60)
    print("مثال 5: رسم النتائج")
    print("=" * 60)
    
    np.random.seed(42)
    cities = [(np.random.rand() * 100, np.random.rand() * 100) for _ in range(12)]
    
    solver = TSPGeoAttention(cities, grid_size=3)
    tour = solver.solve()
    dist = solver.get_tour_distance(tour)
    
    # رسم النتيجة
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # رسم المدن
    xs, ys = zip(*cities)
    ax.scatter(xs, ys, c='blue', s=100, zorder=5, edgecolors='black', linewidth=1.5)
    
    # رسم المسار
    tour_points = [cities[i] for i in tour] + [cities[tour[0]]]
    tx, ty = zip(*tour_points)
    ax.plot(tx, ty, 'r--', linewidth=2, alpha=0.8, label='المسار')
    
    # رسم شبكة التقسيم
    for i in range(solver.grid_size + 1):
        ax.axvline(solver.min_x + i * solver.cell_width, color='gray', linestyle=':', alpha=0.3)
        ax.axhline(solver.min_y + i * solver.cell_height, color='gray', linestyle=':', alpha=0.3)
    
    ax.set_title(f"TSP-GeoAttention Solution\nDistance: {dist:.2f}", fontsize=14, fontweight='bold')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('tsp_solution.png', dpi=150, bbox_inches='tight')
    print("✅ تم حفظ الرسم في: tsp_solution.png")
    plt.show()


if __name__ == "__main__":
    print("\n" + "🗺️ " * 20)
    print("أمثلة على استخدام TSP-GeoAttention Solver")
    print("🗺️ " * 20 + "\n")
    
    # تشغيل الأمثلة
    example_1_random_cities()
    example_2_small_problem()
    example_3_different_grid_sizes()
    example_4_distance_types()
    example_5_visualization()
    
    print("\n" + "=" * 60)
    print("✅ انتهت جميع الأمثلة بنجاح!")
    print("=" * 60)

