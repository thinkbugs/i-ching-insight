#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模式学习器 - 从数据中学习卦象模式
功能：数据编码、模式识别、聚类
"""

import argparse
import json
import numpy as np
from collections import defaultdict

class PatternLearner:
    """
    模式学习器
    """
    
    def __init__(self):
        self.patterns = defaultdict(int)
        self.learned = False
    
    def encode_data_to_gua(self, data):
        """
        将数据编码为卦象
        """
        # 简化编码：哈希到0-63
        gua_index = hash(str(data)) % 64
        return {
            "data": str(data)[:50],
            "gua_index": gua_index,
            "binary": bin(gua_index)[2:].zfill(6)
        }
    
    def learn_pattern(self, data_samples):
        """
        学习模式
        """
        for sample in data_samples:
            gua = self.encode_data_to_gua(sample)
            self.patterns[gua["gua_index"]] += 1
        
        self.learned = True
        
        # 统计
        total = len(data_samples)
        pattern_distribution = {}
        for gua, count in self.patterns.items():
            pattern_distribution[gua] = {
                "count": count,
                "frequency": count / total
            }
        
        return {
            "total_samples": total,
            "unique_patterns": len(self.patterns),
            "pattern_distribution": pattern_distribution
        }
    
    def predict_pattern(self, new_data):
        """
        预测模式
        """
        if not self.learned:
            return {"error": "尚未学习模式"}
        
        gua = self.encode_data_to_gua(new_data)
        
        return {
            "new_data": str(new_data)[:50],
            "predicted_gua": gua["gua_index"],
            "pattern_exists": gua["gua_index"] in self.patterns,
            "confidence": self.patterns.get(gua["gua_index"], 0) / len(self.patterns) if self.patterns else 0
        }
    
    def cluster_patterns(self, n_clusters=8):
        """
        模式聚类
        """
        if not self.learned:
            return {"error": "尚未学习模式"}
        
        # 简化聚类：按卦象八卦分组
        clusters = defaultdict(list)
        
        for gua in self.patterns.keys():
            bagua = gua // 8
            clusters[bagua].append(gua)
        
        return {
            "n_clusters": len(clusters),
            "clusters": dict(clusters)
        }

def main():
    parser = argparse.ArgumentParser(description="模式学习器")
    parser.add_argument("--learn", nargs="+", help="学习模式（数据样本）")
    parser.add_argument("--predict", type=str, help="预测模式")
    parser.add_argument("--cluster", action="store_true", help="模式聚类")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    learner = PatternLearner()
    
    if args.learn:
        result = learner.learn_pattern(args.learn)
    elif args.predict:
        result = learner.predict_pattern(args.predict)
    elif args.cluster:
        # 先学习一些示例数据
        sample_data = [f"data_{i}" for i in range(100)]
        learner.learn_pattern(sample_data)
        result = learner.cluster_patterns()
    else:
        # 默认：学习示例数据
        sample_data = [f"data_{i}" for i in range(50)]
        result = learner.learn_pattern(sample_data)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【模式学习器】")
        print("=" * 70)
        
        if "total_samples" in result:
            print(f"\n【模式学习】")
            print(f"  样本数：{result['total_samples']}")
            print(f"  唯一模式数：{result['unique_patterns']}")
            print(f"  模式分布：{len(result['pattern_distribution'])}种模式")
        
        elif "predicted_gua" in result:
            print(f"\n【模式预测】")
            print(f"  新数据：{result['new_data']}")
            print(f"  预测卦象：{result['predicted_gua']}")
            print(f"  模式存在：{'是' if result['pattern_exists'] else '否'}")
            print(f"  置信度：{result['confidence']:.2f}")
        
        elif "n_clusters" in result:
            print(f"\n【模式聚类】")
            print(f"  聚类数：{result['n_clusters']}")
            for cluster_id, guas in result["clusters"].items():
                print(f"  聚类{cluster_id}: {len(guas)}个模式")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
