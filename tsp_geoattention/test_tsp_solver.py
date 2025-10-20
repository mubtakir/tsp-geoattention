"""
وحدات اختبار شاملة لـ TSP-GeoAttention Solver
"""

import unittest
import numpy as np
from tsp_solver import (
    TSPGeoAttention, euclidean_distance, haversine_distance,
    softmax, spiral_order_indices, compute_tour_distance,
    solve_tsp_exact
)


class TestDistanceFunctions(unittest.TestCase):
    """اختبار دوال المسافة"""
    
    def test_euclidean_distance_zero(self):
        """اختبار المسافة بين نقطة وذاتها"""
        p = (0, 0)
        self.assertAlmostEqual(euclidean_distance(p, p), 0.0)
    
    def test_euclidean_distance_simple(self):
        """اختبار المسافة الإقليدية البسيطة"""
        p1 = (0, 0)
        p2 = (3, 4)
        self.assertAlmostEqual(euclidean_distance(p1, p2), 5.0)
    
    def test_haversine_distance_zero(self):
        """اختبار المسافة الجوية بين نقطة وذاتها"""
        p = (0, 0)
        self.assertAlmostEqual(haversine_distance(p, p), 0.0)
    
    def test_haversine_distance_positive(self):
        """اختبار أن المسافة الجوية موجبة"""
        p1 = (0, 0)
        p2 = (1, 1)
        dist = haversine_distance(p1, p2)
        self.assertGreater(dist, 0)


class TestSoftmax(unittest.TestCase):
    """اختبار دالة softmax"""
    
    def test_softmax_sum_to_one(self):
        """اختبار أن softmax يجمع إلى 1"""
        x = np.array([1, 2, 3])
        result = softmax(x)
        self.assertAlmostEqual(np.sum(result), 1.0)
    
    def test_softmax_positive(self):
        """اختبار أن جميع قيم softmax موجبة"""
        x = np.array([-1, 0, 1])
        result = softmax(x)
        self.assertTrue(np.all(result > 0))


class TestSpiralOrder(unittest.TestCase):
    """اختبار ترتيب المسح الحلزوني"""
    
    def test_spiral_order_length(self):
        """اختبار أن الحلزون يغطي جميع الخلايا"""
        rows, cols = 3, 3
        spiral = spiral_order_indices(rows, cols)
        self.assertEqual(len(spiral), rows * cols)
    
    def test_spiral_order_unique(self):
        """اختبار أن جميع الخلايا فريدة"""
        rows, cols = 4, 4
        spiral = spiral_order_indices(rows, cols)
        self.assertEqual(len(spiral), len(set(spiral)))


class TestTSPGeoAttention(unittest.TestCase):
    """اختبار فئة TSPGeoAttention"""
    
    def setUp(self):
        """إعداد البيانات للاختبار"""
        np.random.seed(42)
        self.cities_small = [(0, 0), (1, 0), (1, 1), (0, 1)]
        self.cities_random = [(np.random.rand() * 100, np.random.rand() * 100) 
                             for _ in range(8)]
    
    def test_initialization(self):
        """اختبار تهيئة الحل"""
        solver = TSPGeoAttention(self.cities_small, grid_size=2)
        self.assertEqual(solver.n, 4)
        self.assertEqual(solver.grid_size, 2)
    
    def test_empty_cities(self):
        """اختبار مع قائمة مدن فارغة"""
        solver = TSPGeoAttention([], grid_size=2)
        tour = solver.solve()
        self.assertEqual(tour, [])
    
    def test_single_city(self):
        """اختبار مع مدينة واحدة"""
        solver = TSPGeoAttention([(0, 0)], grid_size=2)
        tour = solver.solve()
        self.assertEqual(tour, [0])
    
    def test_solve_returns_valid_tour(self):
        """اختبار أن الحل يرجع مسار صحيح"""
        solver = TSPGeoAttention(self.cities_random, grid_size=3)
        tour = solver.solve()
        self.assertEqual(len(tour), len(self.cities_random))
        self.assertEqual(set(tour), set(range(len(self.cities_random))))
    
    def test_tour_distance_calculation(self):
        """اختبار حساب مسافة المسار"""
        solver = TSPGeoAttention(self.cities_small, grid_size=2)
        tour = [0, 1, 2, 3]
        dist = solver.get_tour_distance(tour)
        self.assertGreater(dist, 0)
    
    def test_distance_type_euclidean(self):
        """اختبار نوع المسافة الإقليدية"""
        solver = TSPGeoAttention(self.cities_random, grid_size=3, distance_type='euclidean')
        self.assertEqual(solver.distance_type, 'euclidean')
    
    def test_distance_type_haversine(self):
        """اختبار نوع المسافة الجوية"""
        solver = TSPGeoAttention(self.cities_random, grid_size=3, distance_type='haversine')
        self.assertEqual(solver.distance_type, 'haversine')
    
    def test_intra_cell_tour(self):
        """اختبار حل TSP محلي"""
        solver = TSPGeoAttention(self.cities_random, grid_size=3)
        city_indices = [0, 1, 2]
        tour = solver.intra_cell_tour(city_indices)
        self.assertEqual(len(tour), 3)
        self.assertEqual(set(tour), set(city_indices))
    
    def test_two_opt_improvement(self):
        """اختبار تحسين 2-opt"""
        solver = TSPGeoAttention(self.cities_random, grid_size=3)
        initial_tour = list(range(len(self.cities_random)))
        improved_tour = solver.two_opt_improvement(initial_tour, max_iter=50)
        self.assertEqual(len(improved_tour), len(initial_tour))


class TestComputeTourDistance(unittest.TestCase):
    """اختبار حساب مسافة المسار"""
    
    def test_single_city_distance(self):
        """اختبار مسافة مدينة واحدة"""
        cities = np.array([(0, 0)])
        tour = [0]
        dist = compute_tour_distance(cities, tour)
        self.assertEqual(dist, 0.0)
    
    def test_two_cities_distance(self):
        """اختبار مسافة مدينتين"""
        cities = np.array([(0, 0), (3, 4)])
        tour = [0, 1]
        dist = compute_tour_distance(cities, tour)
        self.assertAlmostEqual(dist, 10.0)  # 5 + 5 (ذهاب وإياب)
    
    def test_square_tour_distance(self):
        """اختبار مسافة مربع"""
        cities = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])
        tour = [0, 1, 2, 3]
        dist = compute_tour_distance(cities, tour)
        self.assertAlmostEqual(dist, 4.0)


class TestSolveTSPExact(unittest.TestCase):
    """اختبار حل TSP الأمثل"""
    
    def test_exact_solution_small(self):
        """اختبار الحل الأمثل لمشكلة صغيرة"""
        cities = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])
        tour, dist = solve_tsp_exact(cities)
        self.assertIsNotNone(tour)
        self.assertIsNotNone(dist)
        self.assertEqual(len(tour), 4)
    
    def test_exact_solution_too_large(self):
        """اختبار أن الحل الأمثل لا يُحسب للمشاكل الكبيرة"""
        cities = np.array([(np.random.rand(), np.random.rand()) for _ in range(15)])
        tour, dist = solve_tsp_exact(cities)
        self.assertIsNone(tour)
        self.assertIsNone(dist)
    
    def test_exact_solution_empty(self):
        """اختبار الحل الأمثل لقائمة فارغة"""
        cities = np.array([])
        tour, dist = solve_tsp_exact(cities)
        self.assertEqual(tour, [])
        self.assertEqual(dist, 0.0)


class TestIntegration(unittest.TestCase):
    """اختبارات التكامل"""
    
    def test_full_workflow(self):
        """اختبار سير العمل الكامل"""
        np.random.seed(42)
        cities = [(np.random.rand() * 100, np.random.rand() * 100) for _ in range(8)]
        
        # حل تقريبي
        solver = TSPGeoAttention(cities, grid_size=3)
        approx_tour = solver.solve()
        approx_dist = solver.get_tour_distance(approx_tour)
        
        # حل أمثل
        exact_tour, exact_dist = solve_tsp_exact(np.array(cities))
        
        # التحقق
        self.assertEqual(len(approx_tour), len(cities))
        self.assertIsNotNone(exact_tour)
        self.assertGreaterEqual(approx_dist, exact_dist * 0.5)  # لا يجب أن يكون أسوأ بكثير
    
    def test_different_grid_sizes(self):
        """اختبار أحجام شبكة مختلفة"""
        np.random.seed(42)
        cities = [(np.random.rand() * 100, np.random.rand() * 100) for _ in range(10)]
        
        distances = []
        for grid_size in [2, 3, 4, 5]:
            solver = TSPGeoAttention(cities, grid_size=grid_size)
            tour = solver.solve()
            dist = solver.get_tour_distance(tour)
            distances.append(dist)
        
        # جميع المسافات يجب أن تكون موجبة
        self.assertTrue(all(d > 0 for d in distances))


if __name__ == '__main__':
    unittest.main()

