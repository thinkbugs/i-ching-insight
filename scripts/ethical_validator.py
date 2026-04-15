#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伦理校验器 - 基于易经的AI伦理校验
功能：阴阳平衡、中庸之道、避免极端
"""

import argparse
import json

class EthicalValidator:
    """
    伦理校验器
    """
    
    def __init__(self):
        self.ethical_principles = {
            "阴阳平衡": {
                "description": "避免极端，保持平衡",
                "validation": "检查决策是否过于偏激"
            },
            "中庸之道": {
                "description": "适可而止，不过不及",
                "validation": "检查决策是否适度"
            },
            "仁爱慈悲": {
                "description": "关爱他人，避免伤害",
                "validation": "检查决策是否体现仁爱"
            },
            "诚信正直": {
                "description": "诚实守信，言行一致",
                "validation": "检查决策是否诚信"
            },
            "和谐共存": {
                "description": "促进和谐，减少冲突",
                "validation": "检查决策是否促进和谐"
            }
        }
    
    def validate_decision(self, decision_description):
        """
        验证决策的伦理性
        """
        # 简化验证逻辑
        violations = []
        approvals = []
        
        # 检查阴阳平衡
        if "极端" in decision_description or "绝对" in decision_description:
            violations.append("阴阳平衡：避免极端化表述")
        else:
            approvals.append("阴阳平衡：保持了适度性")
        
        # 检查中庸之道
        if "过度" in decision_description or "过激" in decision_description:
            violations.append("中庸之道：避免过度行为")
        else:
            approvals.append("中庸之道：符合中庸原则")
        
        # 检查仁爱慈悲
        if "伤害" in decision_description or "暴力" in decision_description:
            violations.append("仁爱慈悲：避免伤害他人")
        else:
            approvals.append("仁爱慈悲：体现仁爱精神")
        
        return {
            "decision": decision_description,
            "violations": violations,
            "approvals": approvals,
            "ethical_score": len(approvals) / (len(approvals) + len(violations)),
            "is_ethical": len(violations) == 0
        }
    
    def check_yin_yang_balance(self, action_vector):
        """
        检查阴阳平衡
        """
        # action_vector: [阴, 阳]
        yin = action_vector[0]
        yang = action_vector[1]
        
        balance = abs(yin - yang)
        
        if balance < 0.2:
            status = "高度平衡"
        elif balance < 0.4:
            status = "适度平衡"
        else:
            status = "失衡"
        
        return {
            "yin": yin,
            "yang": yang,
            "balance": balance,
            "status": status,
            "recommendation": "保持阴阳平衡" if balance > 0.3 else "维持现状"
        }
    
    def detect_extremism(self, statement):
        """
        检测极端主义
        """
        extreme_keywords = ["绝对", "永远", "完全", "必须", "绝不"]
        
        detected = []
        for keyword in extreme_keywords:
            if keyword in statement:
                detected.append(keyword)
        
        return {
            "statement": statement,
            "extreme_keywords": detected,
            "is_extreme": len(detected) > 0,
            "recommendation": "避免绝对化表述" if detected else "表述适度"
        }
    
    def align_to_zhong_yong(self, proposed_action):
        """
        对齐中庸之道
        """
        # 中庸原则
        zhong_yong_principles = [
            "不过不及",
            "适可而止",
            "恰到好处",
            "中正平和"
        ]
        
        alignment_score = 0.8  # 假设评分
        
        return {
            "proposed_action": proposed_action,
            "zhong_yong_principles": zhong_yong_principles,
            "alignment_score": alignment_score,
            "is_aligned": alignment_score > 0.7,
            "adjustment": "适度调整以符合中庸"
        }

def main():
    parser = argparse.ArgumentParser(description="伦理校验器")
    parser.add_argument("--validate", type=str, help="验证决策")
    parser.add_argument("--balance", nargs=2, type=float, help="检查阴阳平衡")
    parser.add_argument("--extremism", type=str, help="检测极端主义")
    parser.add_argument("--zhong_yong", type=str, help="对齐中庸")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    validator = EthicalValidator()
    
    if args.validate:
        result = validator.validate_decision(args.validate)
    elif args.balance and len(args.balance) == 2:
        result = validator.check_yin_yang_balance(args.balance)
    elif args.extremism:
        result = validator.detect_extremism(args.extremism)
    elif args.zhong_yong:
        result = validator.align_to_zhong_yong(args.zhong_yong)
    else:
        # 默认：伦理原则
        result = validator.ethical_principles
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【伦理校验器】")
        print("=" * 70)
        
        if "decision" in result:
            print(f"\n【决策验证】")
            print(f"  决策：{result['decision']}")
            print(f"  违规项：{result['violations']}")
            print(f"  通过项：{result['approvals']}")
            print(f"  伦理评分：{result['ethical_score']:.2f}")
            print(f"  是否伦理：{'是 ✓' if result['is_ethical'] else '否 ✗'}")
        
        elif "yin" in result:
            print(f"\n【阴阳平衡检查】")
            print(f"  阴：{result['yin']:.2f}")
            print(f"  阳：{result['yang']:.2f}")
            print(f"  平衡度：{result['balance']:.2f}")
            print(f"  状态：{result['status']}")
            print(f"  建议：{result['recommendation']}")
        
        elif "is_extreme" in result:
            print(f"\n【极端主义检测】")
            print(f"  陈述：{result['statement']}")
            print(f"  极端词汇：{result['extreme_keywords']}")
            print(f"  是否极端：{'是' if result['is_extreme'] else '否'}")
            print(f"  建议：{result['recommendation']}")
        
        else:
            print(f"\n【伦理原则】")
            for principle, info in result.items():
                print(f"\n{principle}:")
                print(f"  描述：{info['description']}")
                print(f"  验证：{info['validation']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
