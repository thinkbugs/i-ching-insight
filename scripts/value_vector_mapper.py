#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价值向量映射器 - 将卦象映射为价值取向
功能：64卦作为AI价值观基向量
"""

import argparse
import json
import numpy as np

# 64卦价值向量（简化版）
GUA_VALUE_VECTORS = {
    0: [0.9, 0.1, 0.5, 0.2, 0.3, 0.1, 0.8, 0.2],  # 坤：包容、承载
    63: [0.1, 0.9, 0.5, 0.8, 0.7, 0.9, 0.2, 0.8], # 乾：刚健、进取
    11: [0.5, 0.5, 0.9, 0.5, 0.5, 0.5, 0.5, 0.5], # 泰：平衡、和谐
    29: [0.3, 0.7, 0.2, 0.3, 0.4, 0.6, 0.3, 0.4], # 坎：险陷、隐忍
}

class ValueVectorMapper:
    """
    价值向量映射器
    """
    
    def __init__(self):
        self.value_dimensions = [
            "合作", "竞争", "平衡", "创新", "稳定",
            "效率", "公平", "自由"
        ]
        self.gua_vectors = GUA_VALUE_VECTORS
    
    def get_gua_value_vector(self, gua_index):
        """
        获取卦象的价值向量
        """
        if gua_index not in self.gua_vectors:
            # 生成默认向量
            vector = [0.5] * 8
            vector[gua_index % 8] = 0.8
            self.gua_vectors[gua_index] = vector
        
        return {
            "gua_index": gua_index,
            "value_dimensions": self.value_dimensions,
            "value_vector": self.gua_vectors[gua_index],
            "dominant_values": self._get_dominant_values(self.gua_vectors[gua_index])
        }
    
    def _get_dominant_values(self, vector):
        """
        获取主导价值
        """
        dominant = []
        for i, value in enumerate(vector):
            if value > 0.7:
                dominant.append(self.value_dimensions[i])
        return dominant
    
    def calculate_value_distance(self, gua1, gua2):
        """
        计算价值距离
        """
        vec1 = np.array(self.gua_vectors.get(gua1, [0.5] * 8))
        vec2 = np.array(self.gua_vectors.get(gua2, [0.5] * 8))
        
        # 欧氏距离
        euclidean_dist = np.linalg.norm(vec1 - vec2)
        
        # 余弦相似度
        cosine_sim = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
        
        return {
            "gua1": gua1,
            "gua2": gua2,
            "euclidean_distance": euclidean_dist,
            "cosine_similarity": cosine_sim,
            "value_alignment": "高度一致" if cosine_sim > 0.8 else "中度一致" if cosine_sim > 0.5 else "不一致"
        }
    
    def composite_value_vector(self, gua_weights):
        """
        复合价值向量
        """
        composite = np.zeros(8)
        
        for gua, weight in gua_weights.items():
            vec = np.array(self.gua_vectors.get(gua, [0.5] * 8))
            composite += weight * vec
        
        # 归一化
        composite = composite / np.sum(composite)
        
        return {
            "gua_weights": gua_weights,
            "composite_vector": composite.tolist(),
            "dominant_values": self._get_dominant_values(composite.tolist())
        }
    
    def align_to_human_values(self, ai_vector):
        """
        对齐人类价值观
        """
        # 人类价值基准
        human_baseline = np.array([0.6, 0.4, 0.7, 0.5, 0.6, 0.5, 0.8, 0.6])
        
        ai_vec = np.array(ai_vector)
        
        # 对齐误差
        alignment_error = np.linalg.norm(ai_vec - human_baseline)
        
        # 对齐策略
        aligned_vector = ai_vec + 0.5 * (human_baseline - ai_vec)
        
        return {
            "ai_vector": ai_vector.tolist(),
            "human_baseline": human_baseline.tolist(),
            "alignment_error": alignment_error,
            "aligned_vector": aligned_vector.tolist(),
            "is_aligned": alignment_error < 0.3
        }

def main():
    parser = argparse.ArgumentParser(description="价值向量映射器")
    parser.add_argument("--gua", type=int, help="获取卦象价值向量")
    parser.add_argument("--distance", nargs=2, type=int, help="计算价值距离")
    parser.add_argument("--composite", type=str, help="复合价值向量（JSON格式）")
    parser.add_argument("--align", type=str, help="对齐人类价值观（JSON格式的AI向量）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    mapper = ValueVectorMapper()
    
    if args.gua is not None:
        result = mapper.get_gua_value_vector(args.gua)
    elif args.distance and len(args.distance) == 2:
        result = mapper.calculate_value_distance(args.distance[0], args.distance[1])
    elif args.composite:
        try:
            weights = json.loads(args.composite)
            result = mapper.composite_value_vector(weights)
        except:
            result = {"error": "JSON格式错误"}
    elif args.align:
        try:
            ai_vec = json.loads(args.align)
            result = mapper.align_to_human_values(ai_vec)
        except:
            result = {"error": "JSON格式错误"}
    else:
        # 默认：乾卦价值向量
        result = mapper.get_gua_value_vector(63)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【价值向量映射】")
        print("=" * 70)
        
        if "value_vector" in result:
            print(f"\n【卦象价值向量】")
            print(f"  卦象索引：{result['gua_index']}")
            print(f"  价值维度：{result['value_dimensions']}")
            print(f"  价值向量：{result['value_vector']}")
            print(f"  主导价值：{result['dominant_values']}")
        
        elif "euclidean_distance" in result:
            print(f"\n【价值距离】")
            print(f"  卦象1：{result['gua1']}")
            print(f"  卦象2：{result['gua2']}")
            print(f"  欧氏距离：{result['euclidean_distance']:.4f}")
            print(f"  余弦相似度：{result['cosine_similarity']:.4f}")
            print(f"  价值对齐：{result['value_alignment']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
