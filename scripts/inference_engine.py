#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推理引擎 - 基于卦象的逻辑推理
功能：符号推理、概率推理、因果推理
"""

import argparse
import json

class InferenceEngine:
    """
    推理引擎
    """
    
    def __init__(self):
        self.knowledge_base = {}
        self.rules = {}
    
    def add_fact(self, fact, value):
        """
        添加事实
        """
        self.knowledge_base[fact] = value
    
    def add_rule(self, condition, conclusion):
        """
        添加规则
        """
        if condition not in self.rules:
            self.rules[condition] = []
        self.rules[condition].append(conclusion)
    
    def symbolic_reasoning(self, query):
        """
        符号推理
        """
        # 简化推理：正向链
        results = []
        
        for condition, conclusions in self.rules.items():
            if condition in self.knowledge_base and self.knowledge_base[condition]:
                for conclusion in conclusions:
                    results.append(conclusion)
        
        return {
            "query": query,
            "reasoning_type": "符号推理",
            "premises": list(self.knowledge_base.keys()),
            "conclusions": results
        }
    
    def probabilistic_reasoning(self, hypothesis, evidence):
        """
        概率推理
        """
        # 贝叶斯推理（简化）
        # P(H|E) = P(E|H) * P(H) / P(E)
        
        P_H = 0.5  # 先验概率
        P_E_given_H = 0.8  # 似然
        P_E = 0.6  # 证据概率
        
        P_H_given_E = (P_E_given_H * P_H) / P_E
        
        return {
            "hypothesis": hypothesis,
            "evidence": evidence,
            "prior_probability": P_H,
            "likelihood": P_E_given_H,
            "posterior_probability": P_H_given_E,
            "confidence": P_H_given_E
        }
    
    def causal_reasoning(self, effect):
        """
        因果推理
        """
        # 简化因果图
        causal_graph = {
            "乾卦": ["成功", "领导"],
            "坤卦": ["失败", "顺从"],
            "坎卦": ["危险", "机遇"]
        }
        
        possible_causes = []
        for cause, effects in causal_graph.items():
            if effect in effects:
                possible_causes.append(cause)
        
        return {
            "effect": effect,
            "possible_causes": possible_causes,
            "reasoning": "从效果回溯原因"
        }
    
    def yao_bian_reasoning(self, current_gua, moving_yao):
        """
        爻变推理
        """
        # 爻变推演
        binary = bin(current_gua)[2:].zfill(6)
        
        # 应用爻变
        changed_binary = list(binary)
        for yao in moving_yao:
            if 0 <= yao < 6:
                changed_binary[yao] = '1' if changed_binary[yao] == '0' else '0'
        
        new_gua = int(''.join(changed_binary), 2)
        
        return {
            "current_gua": current_gua,
            "moving_yao": moving_yao,
            "original_binary": binary,
            "changed_binary": ''.join(changed_binary),
            "new_gua": new_gua,
            "reasoning_chain": [
                f"当前卦象：{binary}",
                f"动爻：{moving_yao}",
                f"爻变后：{''.join(changed_binary)}",
                f"之卦：{new_gua}"
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="推理引擎")
    parser.add_argument("--symbolic", type=str, help="符号推理查询")
    parser.add_argument("--probabilistic", nargs=2, help="概率推理（假设 证据）")
    parser.add_argument("--causal", type=str, help="因果推理（效果）")
    parser.add_argument("--yao_bian", nargs=2, help="爻变推理（卦象 动爻列表）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    engine = InferenceEngine()
    
    # 添加示例知识
    engine.add_fact("乾卦", True)
    engine.add_fact("坤卦", False)
    engine.add_rule("乾卦", "成功")
    engine.add_rule("坤卦", "顺从")
    
    if args.symbolic:
        result = engine.symbolic_reasoning(args.symbolic)
    elif args.probabilistic and len(args.probabilistic) == 2:
        result = engine.probabilistic_reasoning(args.probabilistic[0], args.probabilistic[1])
    elif args.causal:
        result = engine.causal_reasoning(args.causal)
    elif args.yao_bian and len(args.yao_bian) == 2:
        gua = int(args.yao_bian[0])
        yao = list(map(int, args.yao_bian[1].split(',')))
        result = engine.yao_bian_reasoning(gua, yao)
    else:
        # 默认：爻变推理
        result = engine.yao_bian_reasoning(0, [0, 1])
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【推理引擎】")
        print("=" * 70)
        
        if "reasoning_type" in result:
            print(f"\n【符号推理】")
            print(f"  查询：{result['query']}")
            print(f"  前提：{result['premises']}")
            print(f"  结论：{result['conclusions']}")
        
        elif "posterior_probability" in result:
            print(f"\n【概率推理】")
            print(f"  假设：{result['hypothesis']}")
            print(f"  证据：{result['evidence']}")
            print(f"  先验概率：{result['prior_probability']:.2f}")
            print(f"  后验概率：{result['posterior_probability']:.2f}")
            print(f"  置信度：{result['confidence']:.2f}")
        
        elif "possible_causes" in result:
            print(f"\n【因果推理】")
            print(f"  效果：{result['effect']}")
            print(f"  可能原因：{result['possible_causes']}")
            print(f"  推理：{result['reasoning']}")
        
        elif "reasoning_chain" in result:
            print(f"\n【爻变推理】")
            for step in result["reasoning_chain"]:
                print(f"  {step}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
