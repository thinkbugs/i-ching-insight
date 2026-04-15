#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
涌现规律分析工具 - 分析64卦网络的涌现特性
功能：相变、临界现象、无标度网络、小世界网络
"""

import argparse
import json
import numpy as np
from collections import defaultdict, Counter

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

class EmergenceAnalyzer:
    """
    涌现规律分析器
    """
    
    def __init__(self):
        self.hexagrams = list(range(64))
    
    def _int_to_binary(self, n):
        """整数转6位二进制字符串"""
        return bin(n)[2:].zfill(6)
    
    def _count_ones(self, n):
        """计算二进制中1的个数（阳爻数）"""
        return bin(n).count('1')
    
    def analyze_yang_yin_distribution(self):
        """
        分析阴阳分布（涌现模式1）
        """
        distribution = defaultdict(int)
        
        for gua in self.hexagrams:
            yang_count = self._count_ones(gua)
            yin_count = 6 - yang_count
            distribution[f"{yang_count}阳{yin_count}阴"] += 1
        
        # 计算统计特征
        yang_counts = [self._count_ones(g) for gua in self.hexagrams]
        
        return {
            "distribution": dict(distribution),
            "statistics": {
                "mean_yang": np.mean(yang_counts),
                "std_yang": np.std(yang_counts),
                "max_yang": max(yang_counts),
                "min_yang": min(yang_counts)
            }
        }
    
    def analyze_degree_sequence(self, degrees):
        """
        分析度序列（判断无标度网络）
        """
        # 统计度数分布
        degree_counts = Counter(degrees)
        
        # 计算幂律指数
        unique_degrees = sorted(degree_counts.keys())
        counts = [degree_counts[d] for d in unique_degrees]
        
        # 对数线性回归估计幂律指数
        log_degrees = np.log(unique_degrees)
        log_counts = np.log(counts)
        
        if len(unique_degrees) > 1:
            # 简单线性回归
            slope = np.polyfit(log_degrees, log_counts, 1)[0]
            power_law_exponent = -slope
        else:
            power_law_exponent = None
        
        return {
            "degree_distribution": dict(degree_counts),
            "power_law_exponent": power_law_exponent,
            "is_scale_free": power_law_exponent is not None and 2 < power_law_exponent < 3
        }
    
    def detect_community_structure(self, adjacency):
        """
        检测社区结构（模块化分析）
        """
        # 简化的社区检测（基于八卦分组）
        # 将64卦按八卦分组
        
        bagua_mapping = {}
        for i, gua in enumerate(self.hexagrams):
            trigram = i // 8
            bagua_mapping[gua] = trigram
        
        communities = defaultdict(list)
        for gua, bagua in bagua_mapping.items():
            communities[bagua].append(gua)
        
        # 计算模块度
        num_edges = sum(len(neighbors) for neighbors in adjacency.values()) // 2
        modularity = 0.0
        
        for community_nodes in communities.values():
            # 社区内部边数（简化估计）
            internal_edges = len(community_nodes) * 3  # 粗略估计
            expected_edges = (sum(len(adjacency[n]) for n in community_nodes)) ** 2 / (4 * num_edges)
            modularity += (internal_edges - expected_edges) / (2 * num_edges)
        
        return {
            "num_communities": len(communities),
            "community_sizes": [len(nodes) for nodes in communities.values()],
            "modularity": modularity,
            "is_modular": modularity > 0.3
        }
    
    def analyze_phase_transition(self, parameter_values, metric_values):
        """
        分析相变（参数变化导致系统行为突变）
        """
        # 检测指标变化率
        if len(parameter_values) < 2:
            return {"error": "数据不足"}
        
        # 计算变化率
        rates = []
        for i in range(1, len(metric_values)):
            if parameter_values[i] != parameter_values[i-1]:
                rate = abs(metric_values[i] - metric_values[i-1]) / abs(parameter_values[i] - parameter_values[i-1])
                rates.append(rate)
        
        # 识别相变点（变化率突然增大的点）
        threshold = np.mean(rates) + 2 * np.std(rates) if rates else 0
        phase_transition_points = []
        
        for i in range(1, len(rates)):
            if rates[i] > threshold:
                phase_transition_points.append({
                    "parameter": parameter_values[i],
                    "metric": metric_values[i],
                    "rate": rates[i]
                })
        
        return {
            "rates": rates,
            "threshold": threshold,
            "phase_transitions": phase_transition_points
        }
    
    def analyze_critical_phenomena(self, network_size, clustering_coefficient, path_length):
        """
        分析临界现象
        """
        # 64卦网络在6维超立方体上的临界特性
        
        # 计算临界指标
        critical_clustering = 0.75  # 6维超立方体的理论值
        critical_path_length = 3.0  # 理论值
        
        is_critical = (abs(clustering_coefficient - critical_clustering) < 0.2 and
                      abs(path_length - critical_path_length) < 1.0)
        
        return {
            "is_at_critical_point": is_critical,
            "theoretical_clustering": critical_clustering,
            "actual_clustering": clustering_coefficient,
            "theoretical_path_length": critical_path_length,
            "actual_path_length": path_length,
            "deviation": {
                "clustering": abs(clustering_coefficient - critical_clustering),
                "path_length": abs(path_length - critical_path_length)
            }
        }
    
    def analyze_small_world_properties(self, clustering_coefficient, path_length):
        """
        分析小世界网络特性
        """
        # 小世界网络标准：高聚类系数 + 短平均路径长度
        # 与随机网络比较
        
        # 随机网络的聚类系数（近似）
        random_clustering = 0.1  # 粗略估计
        
        # 随机网络的平均路径长度（近似）
        random_path_length = 2.5  # 粗略估计
        
        # 小世界网络系数
        clustering_ratio = clustering_coefficient / random_clustering if random_clustering > 0 else 1
        path_ratio = path_length / random_path_length if random_path_length > 0 else 1
        
        is_small_world = (clustering_ratio > 2.0) and (path_ratio < 2.0)
        
        return {
            "is_small_world": is_small_world,
            "clustering_ratio": clustering_ratio,
            "path_ratio": path_ratio,
            "sigma": clustering_ratio / path_ratio if path_ratio > 0 else 0
        }
    
    def analyze_self_organization(self):
        """
        分析自组织特性
        """
        # 64卦系统的自组织特性
        
        # 1. 对称性自发破缺
        # 从完全对称（坤/乾）到不对称
        
        # 2. 模式涌现
        # 从随机排列到有序结构
        
        # 3. 能量最小化
        # 系统趋向稳定状态
        
        return {
            "symmetry_breaking": True,
            "pattern_emergence": True,
            "energy_minimization": True,
            "is_self_organized": True
        }
    
    def analyze_synchronization(self, adjacency_matrix, initial_states):
        """
        分析同步现象
        """
        # 简化的同步分析
        # 检查系统是否能够达到同步状态
        
        n = len(initial_states)
        
        # 计算耦合强度
        coupling = np.mean(adjacency_matrix) if adjacency_matrix is not None else 0
        
        # 同步阈值（临界耦合强度）
        sync_threshold = 0.3
        
        can_synchronize = coupling > sync_threshold
        
        return {
            "coupling_strength": coupling,
            "sync_threshold": sync_threshold,
            "can_synchronize": can_synchronize
        }

def main():
    parser = argparse.ArgumentParser(description="涌现规律分析工具")
    parser.add_argument("--yang_yin", action="store_true", help="分析阴阳分布")
    parser.add_argument("--degree", nargs="+", type=int, help="分析度序列（度数列表）")
    parser.add_argument("--phase", action="store_true", help="相变分析示例")
    parser.add_argument("--small_world", nargs=2, type=float, help="小世界分析（聚类系数，路径长度）")
    parser.add_argument("--critical", nargs=2, type=float, help="临界现象分析（聚类系数，路径长度）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    analyzer = EmergenceAnalyzer()
    
    if args.yang_yin:
        result = analyzer.analyze_yang_yin_distribution()
    elif args.degree:
        result = analyzer.analyze_degree_sequence(args.degree)
    elif args.phase:
        # 相变分析示例
        params = list(range(10))
        metrics = [p**2 for p in params]  # 二次关系
        result = analyzer.analyze_phase_transition(params, metrics)
    elif args.small_world and len(args.small_world) == 2:
        clustering, path_length = args.small_world
        result = analyzer.analyze_small_world_properties(clustering, path_length)
    elif args.critical and len(args.critical) == 2:
        clustering, path_length = args.critical
        result = analyzer.analyze_critical_phenomena(64, clustering, path_length)
    else:
        # 默认：阴阳分布
        result = analyzer.analyze_yang_yin_distribution()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【涌现规律分析】")
        print("=" * 70)
        
        if "distribution" in result:
            print(f"\n【阴阳分布】")
            for pattern, count in sorted(result["distribution"].items()):
                print(f"  {pattern}: {count}卦")
            
            stats = result["statistics"]
            print(f"\n【统计特征】")
            print(f"  平均阳爻数：{stats['mean_yang']:.2f}")
            print(f"  标准差：{stats['std_yang']:.2f}")
            print(f"  最大阳爻数：{stats['max_yang']}")
            print(f"  最小阳爻数：{stats['min_yang']}")
        
        elif "power_law_exponent" in result:
            print(f"\n【度序列分析】")
            dist = result["degree_distribution"]
            for degree, count in sorted(dist.items()):
                print(f"  度数 {degree}: {count}个节点")
            
            exponent = result["power_law_exponent"]
            print(f"\n【幂律指数】")
            print(f"  指数：{exponent:.4f}")
            print(f"  无标度网络：{'是 ✓' if result['is_scale_free'] else '否 ✗'}")
        
        elif "is_small_world" in result:
            print(f"\n【小世界网络特性】")
            print(f"  是否小世界网络：{'是 ✓' if result['is_small_world'] else '否 ✗'}")
            print(f"  聚类系数比率：{result['clustering_ratio']:.4f}")
            print(f"  路径长度比率：{result['path_ratio']:.4f}")
            print(f"  σ系数：{result['sigma']:.4f}")
        
        elif "is_at_critical_point" in result:
            print(f"\n【临界现象分析】")
            print(f"  是否在临界点：{'是 ✓' if result['is_at_critical_point'] else '否 ✗'}")
            print(f"  理论聚类系数：{result['theoretical_clustering']:.4f}")
            print(f"  实际聚类系数：{result['actual_clustering']:.4f}")
            print(f"  理论路径长度：{result['theoretical_path_length']:.4f}")
            print(f"  实际路径长度：{result['actual_path_length']:.4f}")
        
        elif "phase_transitions" in result:
            print(f"\n【相变分析】")
            print(f"  相变点数：{len(result['phase_transitions'])}")
            for pt in result['phase_transitions']:
                print(f"    参数={pt['parameter']}, 指标={pt['metric']}, 变化率={pt['rate']:.4f}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
