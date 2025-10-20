"""
TSP-GeoAttention Solver
========================
حل هجين مبتكر لمسألة البائع المتجول (TSP)
يجمع بين: الهندسة المكانية + مبدأ الفعل الأدنى + آلية الانتباه

الباحث: باسل يحيى عبدالله
"""

import numpy as np
import math
from itertools import permutations
from typing import List, Tuple, Optional
import re


# ==================== وظائف مساعدة ====================

def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """حساب المسافة الإقليدية بين نقطتين"""
    return np.linalg.norm(np.array(p1) - np.array(p2))


def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    حساب المسافة الجوية (Great-circle) بين نقطتين
    coord = (lon, lat) بالدرجات
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # نصف قطر الأرض بالكيلومتر
    return c * r


def softmax(x: np.ndarray) -> np.ndarray:
    """تطبيق دالة softmax مع تجنب overflow"""
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum()


def spiral_order_indices(rows: int, cols: int) -> List[Tuple[int, int]]:
    """
    توليد ترتيب حلزوني من المحيط إلى المركز
    """
    visited = [[False] * cols for _ in range(rows)]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c, d = 0, 0, 0
    spiral = []
    
    for _ in range(rows * cols):
        spiral.append((r, c))
        visited[r][c] = True
        nr, nc = r + directions[d][0], c + directions[d][1]
        if not (0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]):
            d = (d + 1) % 4
            nr, nc = r + directions[d][0], c + directions[d][1]
        r, c = nr, nc
    return spiral


def compute_tour_distance(cities: np.ndarray, tour: List[int], 
                         distance_func=euclidean_distance) -> float:
    """حساب المسافة الكلية للمسار"""
    if len(tour) <= 1:
        return 0.0
    total = 0.0
    n = len(tour)
    for i in range(n):
        total += distance_func(cities[tour[i]], cities[tour[(i+1) % n]])
    return total


def read_tsplib(filename: str) -> List[Tuple[float, float]]:
    """قراءة ملف TSPLIB بتنسيق بسيط"""
    cities = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_section = False
    for line in lines:
        line = line.strip()
        if line == "NODE_COORD_SECTION":
            in_section = True
            continue
        if line == "EOF" or line.startswith("DISPLAY_DATA_SECTION"):
            break
        if in_section:
            parts = re.split(r'\s+', line)
            if len(parts) >= 3:
                x = float(parts[1])
                y = float(parts[2])
                cities.append((x, y))
    
    if not cities:
        raise ValueError("لم يتم العثور على إحداثيات في الملف.")
    
    return cities


def solve_tsp_exact(cities: np.ndarray) -> Tuple[Optional[List[int]], Optional[float]]:
    """حل TSP بشكل أمثل باستخدام التباديل (لـ n <= 10)"""
    n = len(cities)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0
    if n > 10:
        return None, None
    
    best_tour = None
    best_dist = float('inf')
    
    for perm in permutations(range(n)):
        dist = compute_tour_distance(cities, perm)
        if dist < best_dist:
            best_dist = dist
            best_tour = list(perm)
    
    return best_tour, best_dist


# ==================== فئة TSPGeoAttention ====================

class TSPGeoAttention:
    """
    حل هجين لمسألة البائع المتجول
    يستخدم: تقسيم مكاني + مسح حلزوني + انتباه ديناميكي
    """
    
    def __init__(self, cities: List[Tuple[float, float]], 
                 grid_size: int = 5, 
                 distance_type: str = 'euclidean'):
        """
        Args:
            cities: قائمة إحداثيات المدن
            grid_size: حجم الشبكة (عدد الخلايا في كل اتجاه)
            distance_type: 'euclidean' أو 'haversine'
        """
        self.cities = np.array(cities)
        self.n = len(cities)
        self.grid_size = grid_size
        self.distance_type = distance_type
        
        if self.n == 0:
            return
        
        # حساب المربع المحيط
        self.min_x, self.min_y = self.cities.min(axis=0)
        self.max_x, self.max_y = self.cities.max(axis=0)

        # إضافة هامش (تجنب الحالة عندما تكون جميع المدن في نقطة واحدة)
        margin = 0.1 * max(self.max_x - self.min_x, self.max_y - self.min_y, 1.0)
        self.min_x -= margin
        self.min_y -= margin
        self.max_x += margin
        self.max_y += margin

        # تقسيم إلى شبكة
        self.cell_width = max((self.max_x - self.min_x) / grid_size, 1e-6)
        self.cell_height = max((self.max_y - self.min_y) / grid_size, 1e-6)
        
        # تعيين المدن إلى الخلايا
        self.cell_to_cities = {}
        self.city_to_cell = {}
        
        for i, (x, y) in enumerate(self.cities):
            col = min(int((x - self.min_x) / self.cell_width), grid_size - 1)
            row = min(int((y - self.min_y) / self.cell_height), grid_size - 1)
            cell = (row, col)
            if cell not in self.cell_to_cities:
                self.cell_to_cities[cell] = []
            self.cell_to_cities[cell].append(i)
            self.city_to_cell[i] = cell
    
    def _distance(self, p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
        """اختيار دالة المسافة المناسبة"""
        if self.distance_type == 'haversine':
            return haversine_distance(p1, p2)
        return euclidean_distance(p1, p2)
    
    def get_cell_center(self, cell: Tuple[int, int]) -> Tuple[float, float]:
        """حساب مركز الخلية"""
        row, col = cell
        x = self.min_x + (col + 0.5) * self.cell_width
        y = self.min_y + (row + 0.5) * self.cell_height
        return (x, y)
    
    def intra_cell_tour(self, city_indices: List[int]) -> List[int]:
        """حل TSP محلي داخل الخلية باستخدام Nearest Neighbor + Attention"""
        if len(city_indices) <= 1:
            return city_indices
        
        unvisited = set(city_indices)
        tour = [city_indices[0]]
        unvisited.remove(city_indices[0])
        
        while unvisited:
            current = tour[-1]
            scores = []
            candidates = []
            
            for city in unvisited:
                dist = self._distance(self.cities[current], self.cities[city])
                scores.append(-dist)
                candidates.append(city)
            
            probs = softmax(np.array(scores))
            next_city = candidates[np.argmax(probs)]
            tour.append(next_city)
            unvisited.remove(next_city)
        
        return tour
    
    def inter_cell_attention_order(self, cells: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """ترتيب الخلايا باستخدام انتباه بين مراكزها"""
        if len(cells) <= 1:
            return cells
        
        ordered = [cells[0]]
        remaining = set(cells[1:])
        
        while remaining:
            current_cell = ordered[-1]
            current_center = self.get_cell_center(current_cell)
            
            scores = []
            candidates = []
            for cell in remaining:
                center = self.get_cell_center(cell)
                dist = self._distance(current_center, center)
                scores.append(-dist)
                candidates.append(cell)
            
            probs = softmax(np.array(scores))
            next_cell = candidates[np.argmax(probs)]
            ordered.append(next_cell)
            remaining.remove(next_cell)
        
        return ordered
    
    def two_opt_improvement(self, tour: List[int], max_iter: int = 200) -> List[int]:
        """تحسين المسار باستخدام 2-opt"""
        best_tour = tour[:]
        best_distance = compute_tour_distance(self.cities, best_tour, self._distance)
        n = len(tour)
        
        for _ in range(max_iter):
            if n < 4:
                break
            i, j = sorted(np.random.choice(n, 2, replace=False))
            if j - i < 2:
                continue
            new_tour = best_tour[:i] + best_tour[i:j][::-1] + best_tour[j:]
            new_dist = compute_tour_distance(self.cities, new_tour, self._distance)
            if new_dist < best_distance:
                best_tour, best_distance = new_tour, new_dist
        
        return best_tour
    
    def solve(self) -> List[int]:
        """حل المسألة باستخدام الخوارزمية الهجينة"""
        if self.n == 0:
            return []
        
        non_empty_cells = list(self.cell_to_cities.keys())
        if not non_empty_cells:
            return list(range(self.n))
        
        # المسح الحلزوني
        spiral_indices = spiral_order_indices(self.grid_size, self.grid_size)
        spiral_cells = [cell for cell in spiral_indices if cell in self.cell_to_cities]
        remaining_cells = [c for c in non_empty_cells if c not in spiral_cells]
        all_cells_ordered = spiral_cells + remaining_cells
        
        # تحسين ترتيب الخلايا بالانتباه
        final_cell_order = self.inter_cell_attention_order(all_cells_ordered)
        
        # حل TSP محلي في كل خلية
        full_tour = []
        for cell in final_cell_order:
            local_tour = self.intra_cell_tour(self.cell_to_cities[cell])
            full_tour.extend(local_tour)
        
        # تحسين عالمي
        full_tour = self.two_opt_improvement(full_tour, max_iter=200)
        
        return full_tour
    
    def get_tour_distance(self, tour: List[int]) -> float:
        """حساب مسافة المسار"""
        return compute_tour_distance(self.cities, tour, self._distance)

