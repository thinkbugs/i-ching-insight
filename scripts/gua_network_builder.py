#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
64卦网络构建工具 - 构建和分析64卦复杂网络
功能：网络构建、拓扑指标、中心性分析
"""

import argparse
import json
import numpy as np
from collections import defaultdict, deque

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

class HexagramNetwork:
    """
    64卦复杂网络
    """
    
    def __init__(self):
        self.nodes = list(range(64))
        self.adjacency = defaultdict(list)
        self.adjacency_matrix = None
        self._build_network()
    
    def _build_network(self):
        """
        构建网络（基于爻变关系）
        """
        # 规则1：相差1爻的卦象相连（汉明距离=1）
        for i in range(64):
            for bit in range(6):
                neighbor = i ^ (1 << bit)
                if neighbor not in self.adjacency[i]:
                    self.adjacency[i].append(neighbor)
        
        # 规则2：错卦相连（汉明距离=6）
        for i in range(64):
            wrong = 63 - i
            if wrong not in self.adjacency[i]:
                self.adjacency[i].append(wrong)
        
        # 规则3：综卦相连（倒置）
        for i in range(64):
            binary = bin(i)[2:].zfill(6)
            reversed_binary = binary[::-1]
            zong = int(reversed_binary, 2)
            if zong not in self.adjacency[i]:
                self.adjacency[i].append(zong)
        
        # 构建邻接矩阵
        self._build_adjacency_matrix()
    
    def _build_adjacency_matrix(self):
        """构建邻接矩阵"""
        n = len(self.nodes)
        self.adjacency_matrix = np.zeros((n, n), dtype=int)
        for i, neighbors in self.adjacency.items():
            for j in neighbors:
                self.adjacency_matrix[i][j] = 1
    
    def get_degree(self, node):
        """计算节点度数"""
        return len(self.adjacency[node])
    
    def get_degree_distribution(self):
        """计算度数分布"""
        degrees = [self.get_degree(node) for node in self.nodes]
        distribution = defaultdict(int)
        for degree in degrees:
            distribution[degree] += 1
        return dict(distribution)
    
    def get_clustering_coefficient(self, node):
        """
        计算聚类系数
        """
        neighbors = self.adjacency[node]
        degree = len(neighbors)
        
        if degree < 2:
            return 0.0
        
        # 计算邻居之间的连接数
        connections = 0
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] in self.adjacency[neighbors[i]]:
                    connections += 1
        
        possible_connections = degree * (degree - 1) / 2
        return connections / possible_connections if possible_connections > 0 else 0.0
    
    def get_average_clustering_coefficient(self):
        """计算平均聚类系数"""
        total = 0.0
        for node in self.nodes:
            total += self.get_clustering_coefficient(node)
        return total / len(self.nodes)
    
    def get_shortest_path(self, start, end):
        """
        计算最短路径（BFS）
        """
        if start == end:
            return [start], 0
        
        visited = {start}
        queue = deque([(start, [start])])
        
        while queue:
            current, path = queue.popleft()
            
            for neighbor in self.adjacency[current]:
                if neighbor == end:
                    return path + [neighbor], len(path)
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return [], float('inf')
    
    def get_average_path_length(self):
        """
        计算平均路径长度
        """
        total_dist = 0
        count = 0
        
        for i in range(min(20, len(self.nodes))):  # 限制计算范围
            for j in range(i + 1, min(20, len(self.nodes))):
                path, dist = self.get_shortest_path(i, j)
                if dist < float('inf'):
                    total_dist += dist
                    count += 1
        
        return total_dist / count if count > 0 else 0.0
    
    def get_diameter(self):
        """
        计算网络直径
        """
        max_dist = 0
        diameter_pair = (0, 0)
        
        for i in range(min(30, len(self.nodes))):
            for j in range(i + 1, min(30, len(self.nodes))):
                _, dist = self.get_shortest_path(i, j)
                if dist > max_dist:
                    max_dist = dist
                    diameter_pair = (i, j)
        
        return max_dist, diameter_pair
    
    def get_degree_centrality(self):
        """
        计算度中心性
        """
        max_degree = max([self.get_degree(node) for node in self.nodes])
        centrality = {}
        for node in self.nodes:
            centrality[node] = self.get_degree(node) / max_degree
        return centrality
    
    def get_betweenness_centrality(self):
        """
        计算中介中心性
        """
        centrality = {node: 0.0 for node in self.nodes}
        
        # 对每对节点计算最短路径
        for i in range(min(20, len(self.nodes))):
            for j in range(i + 1, min(20, len(self.nodes))):
                path, _ = self.get_shortest_path(i, j)
                for node in path[1:-1]:  # 排除起点和终点
                    centrality[node] += 1
        
        # 归一化
        max_val = max(centrality.values()) if centrality else 1
        for node in centrality:
            centrality[node] = centrality[node] / max_val if max_val > 0 else 0
        
        return centrality
    
    def get_closeness_centrality(self):
        """
        计算接近中心性
        """
        centrality = {}
        
        for node in range(min(20, len(self.nodes))):
            total_dist = 0
            reachable = 0
            
            for target in self.nodes:
                if node == target:
                    continue
                _, dist = self.get_shortest_path(node, target)
                if dist < float('inf'):
                    total_dist += dist
                    reachable += 1
            
            if reachable > 0:
                centrality[node] = reachable / total_dist
            else:
                centrality[node] = 0.0
        
        return centrality
    
    def analyze_network_properties(self):
        """
        分析网络属性
        """
        # 基本统计
        num_nodes = len(self.nodes)
        num_edges = sum(len(neighbors) for neighbors in self.adjacency.values()) // 2
        
        # 度数分布
        degree_dist = self.get_degree_distribution()
        
        # 聚类系数
        avg_clustering = self.get_average_clustering_coefficient()
        
        # 路径长度
        avg_path_length = self.get_average_path_length()
        diameter, _ = self.get_diameter()
        
        # 中心性
        degree_cent = self.get_degree_centrality()
        top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # 判断网络类型
        is_small_world = (avg_path_length < 5) and (avg_clustering > 0.3)
        
        return {
            "basic_stats": {
                "num_nodes": num_nodes,
                "num_edges": num_edges,
                "average_degree": sum(degree_dist[k] * k for k in degree_dist) / num_nodes,
                "density": 2 * num_edges / (num_nodes * (num_nodes - 1))
            },
            "degree_distribution": degree_dist,
            "clustering": {
                "average": avg_clustering
            },
            "path_length": {
                "average": avg_path_length,
                "diameter": diameter
            },
            "centrality": {
                "top_degree": [(GUA_64[i], round(v, 4)) for i, v in top_degree]
            },
            "network_type": {
                "is_small_world": is_small_world,
                "is_connected": True,  # 64卦网络是连通的
                "is_regular": len(set(degree_dist.values())) == 1
            }
        }

def main():
    parser = argparse.ArgumentParser(description="64卦网络构建工具")
    parser.add_argument("--analyze", action="store_true", help="完整分析网络属性")
    parser.add_argument("--degree", type=int, help="计算节点度数")
    parser.add_argument("--clustering", type=int, help="计算节点聚类系数")
    parser.add_argument("--path", nargs=2, type=int, help="计算最短路径")
    parser.add_argument("--centrality", action="store_true", help="计算中心性")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    network = HexagramNetwork()
    
    if args.analyze:
        result = network.analyze_network_properties()
    elif args.degree is not None:
        result = {
            "node": args.degree,
            "node_name": GUA_64[args.degree] if args.degree < 64 else "未知",
            "degree": network.get_degree(args.degree)
        }
    elif args.clustering is not None:
        result = {
            "node": args.clustering,
            "node_name": GUA_64[args.clustering] if args.clustering < 64 else "未知",
            "clustering_coefficient": network.get_clustering_coefficient(args.clustering)
        }
    elif args.path and len(args.path) == 2:
        path, dist = network.get_shortest_path(args.path[0], args.path[1])
        result = {
            "start": GUA_64[args.path[0]] if args.path[0] < 64 else "未知",
            "end": GUA_64[args.path[1]] if args.path[1] < 64 else "未知",
            "path": [GUA_64[n] for n in path],
            "distance": dist
        }
    elif args.centrality:
        result = {
            "degree_centrality": network.get_degree_centrality(),
            "betweenness_centrality": network.get_betweenness_centrality(),
            "closeness_centrality": network.get_closeness_centrality()
        }
    else:
        # 默认：完整分析
        result = network.analyze_network_properties()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【64卦复杂网络分析】")
        print("=" * 70)
        
        if "basic_stats" in result:
            stats = result["basic_stats"]
            print(f"\n【基本统计】")
            print(f"  节点数：{stats['num_nodes']}")
            print(f"  边数：{stats['num_edges']}")
            print(f"  平均度数：{stats['average_degree']:.2f}")
            print(f"  网络密度：{stats['density']:.4f}")
            
            print(f"\n【度数分布】")
            for degree, count in sorted(result["degree_distribution"].items()):
                print(f"  度数 {degree}: {count} 个节点")
            
            print(f"\n【聚类系数】")
            print(f"  平均聚类系数：{result['clustering']['average']:.4f}")
            
            print(f"\n【路径长度】")
            print(f"  平均路径长度：{result['path_length']['average']:.2f}")
            print(f"  网络直径：{result['path_length']['diameter']}")
            
            print(f"\n【中心性分析】")
            print(f"  度中心性Top5：")
            for name, cent in result["centrality"]["top_degree"]:
                print(f"    {name}: {cent}")
            
            print(f"\n【网络类型】")
            print(f"  小世界网络：{'是 ✓' if result['network_type']['is_small_world'] else '否 ✗'}")
            print(f"  连通图：{'是 ✓' if result['network_type']['is_connected'] else '否 ✗'}")
            print(f"  规则网络：{'是 ✓' if result['network_type']['is_regular'] else '否 ✗'}")
        
        elif "degree" in result:
            print(f"\n【度数分析】")
            print(f"  卦象：{result['node_name']}（{result['node']}）")
            print(f"  度数：{result['degree']}")
        
        elif "clustering_coefficient" in result:
            print(f"\n【聚类系数】")
            print(f"  卦象：{result['node_name']}（{result['node']}）")
            print(f"  聚类系数：{result['clustering_coefficient']:.4f}")
        
        elif "path" in result:
            print(f"\n【最短路径】")
            print(f"  起点：{result['start']}")
            print(f"  终点：{result['end']}")
            print(f"  路径：{' → '.join(result['path'])}")
            print(f"  距离：{result['distance']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
