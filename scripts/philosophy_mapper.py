#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
辩证法与阴阳对比工具
功能：正反合、量变质变、否定之否定、对立统一与阴阳的对应
"""

import argparse
import json

class PhilosophyMapper:
    """
    辩证法与阴阳映射器
    """
    
    def __init__(self):
        self.dialectical_laws = self._build_dialectical_laws()
        self.yin_yang_laws = self._build_yin_yang_laws()
    
    def _build_dialectical_laws(self):
        """
        构建辩证法三大规律
        """
        return {
            "对立统一规律": {
                "definition": "矛盾双方既对立又统一",
                "key_concepts": ["对立", "统一", "斗争", "转化"],
                "examples": [
                    "光明与黑暗的对立统一",
                    "生与死的对立统一",
                    "肯定与否定的对立统一"
                ]
            },
            "量变质变规律": {
                "definition": "量变积累到一定程度引起质变",
                "key_concepts": ["量变", "质变", "渐进", "突变"],
                "examples": [
                    "水温升高到100°C沸腾",
                    "知识积累到一定程度产生智慧",
                    "压力积累到临界点爆发革命"
                ]
            },
            "否定之否定规律": {
                "definition": "事物发展呈现螺旋式上升",
                "key_concepts": ["肯定", "否定", "否定之否定", "螺旋上升"],
                "examples": [
                    "麦粒 → 植株 → 更多麦粒",
                    "原始社会 → 奴隶社会 → 封建社会",
                    "感性 → 理性 → 知性"
                ]
            }
        }
    
    def _build_yin_yang_laws(self):
        """
        构建阴阳三大规律
        """
        return {
            "阴阳互根规律": {
                "definition": "阴阳相互依存，不可分割",
                "key_concepts": ["互根", "互用", "相互依存"],
                "examples": [
                    "没有上就没有下",
                    "没有左就没有右",
                    "没有阳就没有阴"
                ]
            },
            "阴阳消长规律": {
                "definition": "阴阳此消彼长，动态平衡",
                "key_concepts": ["消长", "平衡", "动态"],
                "examples": [
                    "日夜交替（阳消阴长）",
                    "四季循环（阴阳转化）",
                    "生命节律（阴阳起伏）"
                ]
            },
            "阴阳转化规律": {
                "definition": "阴阳可以相互转化",
                "key_concepts": ["转化", "临界", "质变"],
                "examples": [
                    "寒极生热，热极生寒",
                    "物极必反",
                    "否极泰来"
                ]
            }
        }
    
    def compare_laws(self):
        """
        对比辩证法与阴阳规律
        """
        return {
            "对立统一 vs 阴阳互根": {
                "dialectics": "矛盾双方既对立又统一",
                "yin_yang": "阴阳相互依存，不可分割",
                "similarity": "都强调对立面的相互关系",
                "difference": "辩证法强调斗争，阴阳强调平衡",
                "integration": "对立统一 + 阴阳平衡 = 系统稳定"
            },
            "量变质变 vs 阴阳消长": {
                "dialectics": "量变积累引起质变",
                "yin_yang": "阴阳消长达到平衡",
                "similarity": "都关注量的变化导致质的变化",
                "difference": "辩证法强调突变，阴阳强调渐进",
                "integration": "量变质变 + 阴阳消长 = 演化规律"
            },
            "否定之否定 vs 阴阳转化": {
                "dialectics": "螺旋式上升",
                "yin_yang": "循环往复",
                "similarity": "都描述事物的发展过程",
                "difference": "辩证法强调上升，阴阳强调循环",
                "integration": "螺旋上升 + 循环往复 = 宇宙演化"
            }
        }
    
    def map_thesis_antithesis_synthesis(self):
        """
        映射正反合到卦象
        """
        return {
            "thesis": {
                "concept": "正题（肯定）",
                "yin_yang": "纯阳（乾卦）",
                "gua": "乾卦（☰☰）",
                "meaning": "原始状态，纯阳刚健",
                "characteristics": ["创造", "主动", "强势"]
            },
            "antithesis": {
                "concept": "反题（否定）",
                "yin_yang": "纯阴（坤卦）",
                "gua": "坤卦（☷☷）",
                "meaning": "否定状态，纯阴柔顺",
                "characteristics": ["接受", "被动", "弱势"]
            },
            "synthesis": {
                "concept": "合题（否定之否定）",
                "yin_yang": "阴阳平衡（泰卦）",
                "gua": "泰卦（☷☰）",
                "meaning": "辩证统一，天地交泰",
                "characteristics": ["平衡", "和谐", "稳定"],
                "higher_level": "螺旋上升，达到新高度"
            }
        }
    
    def map_quantity_quality_change(self):
        """
        映射量变质变到爻变
        """
        return {
            "quantity": {
                "concept": "量变",
                "yin_yang": "爻位渐进",
                "process": "初爻→二爻→三爻→四爻→五爻→上爻",
                "hexagram_example": "复卦（一阳复始）→ 临卦（二阳）→ 泰卦（三阳）→ 大壮卦（四阳）→ 夬卦（五阳）→ 乾卦（六阳）",
                "nature": "渐进积累，逐步增强"
            },
            "quality": {
                "concept": "质变",
                "yin_yang": "卦象突变",
                "critical_point": "从量变到质变的临界点",
                "hexagram_example": "坤卦（纯阴）→ 乾卦（纯阳）的质变",
                "nature": "根本性改变，性质转变"
            },
            "integration": {
                "insight": "量变质变 = 爻变卦变",
                "principle": "量变是爻变，质变是卦变",
                "application": "观察爻位渐进，预判卦象质变"
            }
        }
    
    def map_negation_negation(self):
        """
        映射否定之否定到错综复杂
        """
        return {
            "first_negation": {
                "concept": "第一次否定",
                "yin_yang": "错卦（阴阳全反）",
                "example": "乾卦（☰☰）→ 坤卦（☷☷）",
                "meaning": "从肯定到否定",
                "nature": "根本性否定"
            },
            "second_negation": {
                "concept": "第二次否定（否定之否定）",
                "yin_yang": "综卦（倒置）或之卦（爻变）",
                "example": "坤卦（☷☷）→ 泰卦（☷☰）",
                "meaning": "否定之否定，达到新统一",
                "nature": "螺旋上升"
            },
            "higher_level": {
                "concept": "更高层次",
                "yin_yang": "新的阴阳平衡",
                "example": "从乾到坤再到泰，螺旋上升",
                "insight": "否定之否定 = 循环上升",
                "wisdom": "每一次否定都是进步"
            }
        }
    
    def analyze_unity_opposites(self):
        """
        分析对立统一
        """
        return {
            "opposites": {
                "concept": "对立",
                "yin_yang": "阴阳对立",
                "examples": [
                    "乾卦（阳）vs 坤卦（阴）",
                    "离卦（火）vs 坎卦（水）",
                    "兑卦（泽）vs 艮卦（山）"
                ],
                "nature": "相互排斥，相互斗争"
            },
            "unity": {
                "concept": "统一",
                "yin_yang": "阴阳统一",
                "examples": [
                    "乾坤交泰（泰卦）",
                    "水火既济（既济卦）",
                    "山泽通气（咸卦）"
                ],
                "nature": "相互依存，相互转化"
            },
            "dynamic_balance": {
                "concept": "动态平衡",
                "yin_yang": "阴阳平衡",
                "mechanism": "通过消长达到平衡",
                "insight": "对立统一 = 系统稳定"
            }
        }
    
    def integrate_wisdom(self):
        """
        整合辩证法与阴阳智慧
        """
        return {
            "dialectical_insight": "世界是矛盾的统一体",
            "yin_yang_insight": "万物是阴阳的平衡体",
            "integrated_wisdom": {
                "principle": "矛盾 + 平衡 = 完整系统",
                "application": [
                    "认识矛盾，促进转化",
                    "保持平衡，避免极端",
                    "把握临界，促成飞跃"
                ]
            },
            "practical_guidance": {
                "philosophical": "用辩证法分析矛盾",
                "yin_yang": "用阴阳调节平衡",
                "combined": "辩证分析 + 阴阳调节 = 最佳决策"
            }
        }

def main():
    parser = argparse.ArgumentParser(description="辩证法与阴阳对比")
    parser.add_argument("--laws", action="store_true", help="对比三大规律")
    parser.add_argument("--thesis", action="store_true", help="正反合映射")
    parser.add_argument("--quantity", action="store_true", help="量变质变映射")
    parser.add_argument("--negation", action="store_true", help="否定之否定映射")
    parser.add_argument("--unity", action="store_true", help="对立统一分析")
    parser.add_argument("--wisdom", action="store_true", help="整合智慧")
    parser.add_argument("--all", action="store_true", help="完整对比")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    mapper = PhilosophyMapper()
    
    if args.laws:
        result = mapper.compare_laws()
    elif args.thesis:
        result = mapper.map_thesis_antithesis_synthesis()
    elif args.quantity:
        result = mapper.map_quantity_quality_change()
    elif args.negation:
        result = mapper.map_negation_negation()
    elif args.unity:
        result = mapper.analyze_unity_opposites()
    elif args.wisdom:
        result = mapper.integrate_wisdom()
    elif args.all:
        result = {
            "dialectical_laws": mapper.dialectical_laws,
            "yin_yang_laws": mapper.yin_yang_laws,
            "law_comparison": mapper.compare_laws(),
            "thesis_antithesis_synthesis": mapper.map_thesis_antithesis_synthesis(),
            "quantity_quality_change": mapper.map_quantity_quality_change(),
            "negation_negation": mapper.map_negation_negation(),
            "unity_opposites": mapper.analyze_unity_opposites(),
            "integrated_wisdom": mapper.integrate_wisdom()
        }
    else:
        # 默认：对比三大规律
        result = mapper.compare_laws()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【辩证法与阴阳对比】")
        print("=" * 70)
        
        if "dialectical_laws" in result:
            print(f"\n【辩证法三大规律】")
            for law, content in result["dialectical_laws"].items():
                print(f"\n{law}:")
                print(f"  定义：{content['definition']}")
                print(f"  关键概念：{', '.join(content['key_concepts'])}")
        
        elif "thesis" in result:
            tas = result
            print(f"\n【正反合映射】")
            print(f"\n正题（thesis）：")
            print(f"  阴阳：{tas['thesis']['yin_yang']}")
            print(f"  卦象：{tas['thesis']['gua']}")
            print(f"  含义：{tas['thesis']['meaning']}")
            print(f"\n反题（antithesis）：")
            print(f"  阴阳：{tas['antithesis']['yin_yang']}")
            print(f"  卦象：{tas['antithesis']['gua']}")
            print(f"  含义：{tas['antithesis']['meaning']}")
            print(f"\n合题（synthesis）：")
            print(f"  阴阳：{tas['synthesis']['yin_yang']}")
            print(f"  卦象：{tas['synthesis']['gua']}")
            print(f"  含义：{tas['synthesis']['meaning']}")
            print(f"  更高层次：{tas['synthesis']['higher_level']}")
        
        elif "quantity" in result:
            qq = result
            print(f"\n【量变质变映射】")
            print(f"\n量变（quantity）：")
            print(f"  过程：{qq['quantity']['process']}")
            print(f"  示例：{qq['quantity']['hexagram_example']}")
            print(f"\n质变（quality）：")
            print(f"  临界点：{qq['quality']['critical_point']}")
            print(f"  示例：{qq['quality']['hexagram_example']}")
            print(f"\n整合（integration）：")
            print(f"  洞察：{qq['integration']['insight']}")
        
        elif "unity" in result:
            unity = result
            print(f"\n【对立统一分析】")
            print(f"\n对立（opposites）：")
            print(f"  阴阳：{unity['opposites']['yin_yang']}")
            print(f"  性质：{unity['opposites']['nature']}")
            print(f"\n统一（unity）：")
            print(f"  阴阳：{unity['unity']['yin_yang']}")
            print(f"  性质：{unity['unity']['nature']}")
            print(f"\n动态平衡：")
            print(f"  机制：{unity['dynamic_balance']['mechanism']}")
            print(f"  洞察：{unity['dynamic_balance']['insight']}")
        
        elif "dialectical_insight" in result:
            wisdom = result
            print(f"\n【整合智慧】")
            print(f"  辩证法洞察：{wisdom['dialectical_insight']}")
            print(f"  阴阳洞察：{wisdom['yin_yang_insight']}")
            print(f"  整合原则：{wisdom['integrated_wisdom']['principle']}")
            print(f"  实践指导：{wisdom['practical_guidance']['combined']}")
        
        else:
            for key, value in result.items():
                print(f"\n【{key}】")
                if "dialectics" in value:
                    print(f"  辩证法：{value['dialectics']}")
                if "yin_yang" in value:
                    print(f"  阴阳：{value['yin_yang']}")
                if "integration" in value:
                    print(f"  整合：{value['integration']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
