#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拓扑映射工具 - 揭示卦象空间的拓扑结构
功能：连通性、距离度量、基本群、流形分析
"""

import argparse
import json
import numpy as np
from collections import deque

# 64卦列表
GUA_64 = [
    "坤", "剥", "比", "观", "豫", "晋", "萃", "否",
    "谦", "艮", "蹇", "渐", "小过", "旅", "咸", "遁",
    "师", "蒙", "坎", "涣", "解", "未济", "困", "讼",
    "升", "蛊", "井", "巽", "恒", "鼎", "大过", "姤",
    "复", "颐", "屯", "益", "震", "噬嗑", "随", "无妄",
    "明夷", "贲", "既济", "家人", "丰", "离", "革", "同人",
    "临", "损", "节", "中孚", "归妹", "睽", "兑", "履",
    "泰", "大畜", "需", "小畜", "大壮", "大有", "夬", "乾"
]

class HexagramTopology:
    """
    卦象空间拓扑分析
    """
    
    def __init__(self):
        self.space_size = 64
        self.dimension = 6  # 六爻
        self.adjacency_matrix = None
        self._build_adjacency_matrix()
    
    def _binary_to_int(self, binary_str):
        """二进制字符串转整数"""
        return int(binary_str, 2)
    
    def _int_to_binary(self, n):
        """整数转6位二进制字符串"""
        return bin(n)[2:].zfill(6)
    
    def _build_adjacency_matrix(self):
        """
        构建邻接矩阵（两卦相差1爻为相邻）
        """
        self.adjacency_matrix = np.zeros((self.space_size, self.space_size), dtype=int)
        
        for i in range(self.space_size):
            for j in range(self.space_size):
                # 计算汉明距离（不同爻的数量）
                hamming_dist = self.hamming_distance(i, j)
                if hamming_dist == 1:
                    self.adjacency_matrix[i][j] = 1
    
    def hamming_distance(self, a, b):
        """
        计算汉明距离（两卦相差的爻数）
        """
        diff = a ^ b
        dist = 0
        while diff:
            dist += diff & 1
            diff >>= 1
        return dist
    
    def topological_distance(self, a, b):
        """
        计算拓扑距离（最短路径长度）
        """
        if a == b:
            return 0
        
        # BFS寻找最短路径
        visited = set([a])
        queue = deque([(a, 0)])
        
        while queue:
            node, dist = queue.popleft()
            
            # 遍历所有相邻节点（相差1爻）
            for i in range(self.dimension):
                neighbor = node ^ (1 << i)  # 翻转第i位
                if neighbor == b:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return float('inf')
    
    def get_neighbors(self, node):
        """
        获取相邻节点
        """
        neighbors = []
        for i in range(self.dimension):
            neighbor = node ^ (1 << i)
            neighbors.append(neighbor)
        return neighbors
    
    def analyze_connectivity(self):
        """
        分析连通性
        """
        # 检查图的连通性
        visited = set()
        queue = deque([0])
        visited.add(0)
        
        while queue:
            node = queue.popleft()
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        is_connected = (len(visited) == self.space_size)
        
        # 计算连通分量数
        components = []
        unvisited = set(range(self.space_size))
        
        while unvisited:
            start = unvisited.pop()
            component = set([start])
            queue = deque([start])
            
            while queue:
                node = queue.popleft()
                for neighbor in self.get_neighbors(node):
                    if neighbor not in component:
                        component.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
            unvisited -= component
        
        return {
            "is_connected": is_connected,
            "num_components": len(components),
            "component_sizes": [len(c) for c in components]
        }
    
    def calculate_diameter(self):
        """
        计算图的直径（所有点对最大距离）
        """
        max_dist = 0
        diameter_pair = (0, 0)
        
        for i in range(self.space_size):
            for j in range(i + 1, self.space_size):
                dist = self.topological_distance(i, j)
                if dist > max_dist:
                    max_dist = dist
                    diameter_pair = (i, j)
        
        return {
            "diameter": max_dist,
            "diameter_pair": (GUA_64[diameter_pair[0]], GUA_64[diameter_pair[1]])
        }
    
    def calculate_clustering_coefficient(self, node):
        """
        计算聚类系数
        """
        neighbors = self.get_neighbors(node)
        degree = len(neighbors)
        
        if degree < 2:
            return 0.0
        
        # 计算邻居之间的连接数
        connections = 0
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if self.hamming_distance(neighbors[i], neighbors[j]) == 1:
                    connections += 1
        
        # 聚类系数 = 实际连接数 / 可能的最大连接数
        possible_connections = degree * (degree - 1) / 2
        clustering = connections / possible_connections if possible_connections > 0 else 0.0
        
        return clustering
    
    def average_clustering_coefficient(self):
        """
        计算平均聚类系数
        """
        total = 0.0
        for node in range(self.space_size):
            total += self.calculate_clustering_coefficient(node)
        
        return total / self.space_size
    
    def analyze_local_structure(self, node):
        """
        分析局部拓扑结构
        """
        neighbors = self.get_neighbors(node)
        neighbor_neighbors = []
        
        for n in neighbors:
            nn = self.get_neighbors(n)
            neighbor_neighbors.append(nn)
        
        return {
            "node": node,
            "node_name": GUA_64[node],
            "degree": len(neighbors),
            "neighbors": [GUA_64[n] for n in neighbors],
            "clustering_coefficient": self.calculate_clustering_coefficient(node),
            "local_connectivity": len(set().union(*[set(nn) for nn in neighbor_neighbors]))
        }
    
    def detect_loops(self, max_length=6):
        """
        检测环路（基本群分析）
        """
        loops = []
        
        for start in range(min(10, self.space_size)):  # 限制搜索范围
            # DFS检测环路
            stack = [(start, [start])]
            
            while stack:
                node, path = stack.pop()
                
                if len(path) > max_length:
                    continue
                
                for neighbor in self.get_neighbors(node):
                    if neighbor == start and len(path) >= 3:
                        # 找到环路
                        loops.append(path)
                    elif neighbor not in path:
                        stack.append((neighbor, path + [neighbor]))
        
        return {
            "num_loops": len(loops),
            "loop_lengths": [len(loop) for loop in loops[:10]]  # 只显示前10个
        }
    
    def analyze_manifold_structure(self):
        """
        分析流形结构
        """
        # 欧拉示性数（对于6-维立方体）
        # χ = V - E + F - C + ...
        # 对于n-立方体，χ = 0（n为奇数），χ = 2（n为偶数）
        
        vertices = self.space_size
        edges = np.sum(self.adjacency_matrix) // 2  # 无向边
        
        # 计算3-面（立方体）的数量
        faces_3 = 0  # 3维立方体面
        
        # 欧拉示性数
        euler_characteristic = vertices - edges + faces_3
        
        return {
            "dimension": self.dimension,
            "vertices": vertices,
            "edges": edges,
            "euler_characteristic": euler_characteristic,
            "manifold_type": "6-dimensional hypercube (Q6)",
            "is_compact": True,
            "is_connected": True
        }

def main():
    parser = argparse.ArgumentParser(description="拓扑映射工具")
    parser.add_argument("--connectivity", action="store_true", help="分析连通性")
    parser.add_argument("--distance", nargs=2, type=int, help="计算两卦距离")
    parser.add_argument("--diameter", action="store_true", help="计算图的直径")
    parser.add_argument("--clustering", type=int, help="计算节点的聚类系数")
    parser.add_argument("--loops", action="store_true", help="检测环路")
    parser.add_argument("--manifold", action="store_true", help="分析流形结构")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    topology = HexagramTopology()
    
    if args.connectivity:
        result = topology.analyze_connectivity()
    elif args.distance and len(args.distance) == 2:
        a, b = args.distance
        result = {
            "gua_a": GUA_64[a] if a < 64 else "未知",
            "gua_b": GUA_64[b] if b < 64 else "未知",
            "hamming_distance": topology.hamming_distance(a, b),
            "topological_distance": topology.topological_distance(a, b)
        }
    elif args.diameter:
        result = topology.calculate_diameter()
    elif args.clustering is not None:
        result = topology.analyze_local_structure(args.clustering)
    elif args.loops:
        result = topology.detect_loops()
    elif args.manifold:
        result = topology.analyze_manifold_structure()
    else:
        # 默认：完整分析
        result = {
            "connectivity": topology.analyze_connectivity(),
            "diameter": topology.calculate_diameter(),
            "average_clustering": topology.average_clustering_coefficient(),
            "manifold": topology.analyze_manifold_structure(),
            "loops": topology.detect_loops()
        }
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【卦象空间拓扑分析】")
        print("=" * 70)
        
        if "connectivity" in result:
            conn = result["connectivity"]
            print(f"\n【连通性】")
            print(f"  是否连通：{'是 ✓' if conn['is_connected'] else '否 ✗'}")
            print(f"  连通分量数：{conn['num_components']}")
            print(f"  分量大小：{conn['component_sizes']}")
        
        if "diameter" in result:
            diam = result["diameter"]
            print(f"\n【图的直径】")
            print(f"  直径：{diam['diameter']}")
            print(f"  直径端点：{diam['diameter_pair']}")
        
        if "average_clustering" in result:
            print(f"\n【平均聚类系数】")
            print(f"  值：{result['average_clustering']:.4f}")
        
        if "manifold" in result:
            man = result["manifold"]
            print(f"\n【流形结构】")
            print(f"  维度：{man['dimension']}")
            print(f"  类型：{man['manifold_type']}")
            print(f"  欧拉示性数：{man['euler_characteristic']}")
            print(f"  紧致性：{'是' if man['is_compact'] else '否'}")
        
        if "loops" in result:
            loops = result["loops"]
            print(f"\n【环路检测】")
            print(f"  环路数：{loops['num_loops']}")
            print(f"  环路长度分布：{loops['loop_lengths'][:10]}")
        
        elif "hamming_distance" in result:
            print(f"\n【距离分析】")
            print(f"  卦象A：{result['gua_a']}")
            print(f"  卦象B：{result['gua_b']}")
            print(f"  汉明距离：{result['hamming_distance']}")
            print(f"  拓扑距离：{result['topological_distance']}")
        
        elif "node" in result:
            print(f"\n【局部结构分析】")
            print(f"  卦象：{result['node_name']}（{result['node']}）")
            print(f"  度数：{result['degree']}")
            print(f"  相邻卦象：{', '.join(result['neighbors'])}")
            print(f"  聚类系数：{result['clustering_coefficient']:.4f}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
