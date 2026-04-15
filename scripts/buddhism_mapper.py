#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佛学缘起与卦象映射工具
功能：十二因缘、缘起性空、业力、四圣谛与卦象的对应关系
"""

import argparse
import json

# 十二因缘
TWELVE_LINKS = [
    "无明", "行", "识", "名色", "六入", "触",
    "受", "爱", "取", "有", "生", "老死"
]

# 四圣谛
FOUR_NOBLE_TRUTHS = {
    "苦谛": "生命皆苦",
    "集谛": "苦的成因（渴爱）",
    "灭谛": "苦的止息（涅槃）",
    "道谛": "止苦的路径（八正道）"
}

# 卦象映射
GUA_MAPPING = {
    "苦谛": "坎卦",
    "集谛": "泰卦",
    "灭谛": "乾卦",
    "道谛": "坤卦"
}

class BuddhismMapper:
    """
    佛学与易经映射器
    """
    
    def __init__(self):
        self.twelve_links_mapping = self._build_twelve_links_mapping()
        self.four_truths_mapping = self._build_four_truths_mapping()
    
    def _build_twelve_links_mapping(self):
        """
        构建十二因缘与卦象的映射
        """
        mapping = {}
        
        # 前6支（过去世）
        mapping["无明"] = {
            "gua": "坤卦",
            "gua_index": 0,
            "meaning": "无明 = 全阴，认知蔽障",
            "yin_yang": "纯阴",
            "buddhist_concept": "对实相的误解"
        }
        
        mapping["行"] = {
            "gua": "震卦",
            "gua_index": 51,
            "meaning": "行 = 动作，业力积累",
            "yin_yang": "四阳二阴",
            "buddhist_concept": "基于无明的行为"
        }
        
        mapping["识"] = {
            "gua": "离卦",
            "gua_index": 30,
            "meaning": "识 = 觉知，心识流转",
            "yin_yang": "三阳三阴",
            "buddhist_concept": "意识主体"
        }
        
        mapping["名色"] = {
            "gua": "艮卦",
            "gua_index": 52,
            "meaning": "名色 = 形神，身心形成",
            "yin_yang": "三阴三阳",
            "buddhist_concept": "心理与生理的统一"
        }
        
        mapping["六入"] = {
            "gua": "巽卦",
            "gua_index": 57,
            "meaning": "六入 = 六根，感官门户",
            "yin_yang": "四阳二阴",
            "buddhist_concept": "感官通道"
        }
        
        mapping["触"] = {
            "gua": "兑卦",
            "gua_index": 58,
            "meaning": "触 = 接触，感知对象",
            "yin_yang": "三阳三阴",
            "buddhist_concept": "主客体接触"
        }
        
        # 后6支（现在世）
        mapping["受"] = {
            "gua": "坎卦",
            "gua_index": 29,
            "meaning": "受 = 感受，苦乐舍三受",
            "yin_yang": "二阳四阴",
            "buddhist_concept": "情感体验"
        }
        
        mapping["爱"] = {
            "gua": "咸卦",
            "gua_index": 31,
            "meaning": "爱 = 渴爱，贪著欲望",
            "yin_yang": "三阳三阴",
            "buddhist_concept": "执著与渴求"
        }
        
        mapping["取"] = {
            "gua": "睽卦",
            "gua_index": 38,
            "meaning": "取 = 执取，抓取不放",
            "yin_yang": "三阳三阴",
            "buddhist_concept": "进一步执著"
        }
        
        mapping["有"] = {
            "gua": "大有卦",
            "gua_index": 14,
            "meaning": "有 = 存有，业力成熟",
            "yin_yang": "五阳一阴",
            "buddhist_concept": "业力显化"
        }
        
        mapping["生"] = {
            "gua": "复卦",
            "gua_index": 24,
            "meaning": "生 = 出生，新的轮回",
            "yin_yang": "一阳五阴",
            "buddhist_concept": "新的生命形态"
        }
        
        mapping["老死"] = {
            "gua": "剥卦",
            "gua_index": 23,
            "meaning": "老死 = 衰老死亡",
            "yin_yang": "一阳五阴",
            "buddhist_concept": "生命终结"
        }
        
        return mapping
    
    def _build_four_truths_mapping(self):
        """
        构建四圣谛与卦象的映射
        """
        return {
            "苦谛": {
                "gua": "坎卦",
                "gua_index": 29,
                "description": "生命本质是苦（险陷）",
                "yin_yang": "二阳四阴（阴盛阳衰）",
                "key_points": [
                    "苦的本质 = 险陷（坎卦）",
                    "八苦：生老病死、爱别离、怨憎会、求不得、五蕴炽盛",
                    "易经视角：险而不失其信"
                ]
            },
            "集谛": {
                "gua": "泰卦",
                "gua_index": 11,
                "description": "苦的根源是渴爱（泰而失道）",
                "yin_yang": "三阳三阴（平衡）",
                "key_points": [
                    "集谛 = 贪嗔痴三毒",
                    "易经视角：小往大来，吉亨（贪著）",
                    "苦因 = 阴阳失衡"
                ]
            },
            "灭谛": {
                "gua": "乾卦",
                "gua_index": 63,
                "description": "苦的止息是涅槃（乾道变化）",
                "yin_yang": "六阳（纯阳）",
                "key_points": [
                    "灭谛 = 涅槃寂静",
                    "易经视角：天行健，君子以自强不息",
                    "苦灭 = 回归本源"
                ]
            },
            "道谛": {
                "gua": "坤卦",
                "gua_index": 0,
                "description": "止苦的路径是八正道（厚德载物）",
                "yin_yang": "六阴（纯阴）",
                "key_points": [
                    "道谛 = 八正道（正见、正思维、正语、正业、正命、正精进、正念、正定）",
                    "易经视角：地势坤，君子以厚德载物",
                    "修行 = 涤除阴霾，复归光明"
                ]
            }
        }
    
    def map_conditionality(self):
        """
        映射缘起性空与阴阳变化
        """
        return {
            "conditionality": "此有故彼有，此生故彼生",
            "yin_yang_correspondence": {
                "此有故彼有": "阳生阴长（相互依存）",
                "此生故彼生": "阴阳互根（缘起法则）",
                "此无故彼无": "阴消阳亡（无常变化）",
                "此灭故彼灭": "阴阳转化（循环往复）"
            },
            "emptiness_insight": {
                "concept": "缘起性空",
                "yin_yang_interpretation": "阴阳本空，相待而生",
                "hexagram_manifestation": "六十四卦皆因缘和合",
                "non_self": "卦象无自性，待因缘而显"
            }
        }
    
    def map_karma(self):
        """
        映射业力与爻变因果
        """
        return {
            "karma_definition": "业力 = 意志驱动的行为及其后果",
            "yao_bian_correspondence": {
                "业力因": "初爻动 = 种下业因",
                "业力缘": "中爻变 = 诸缘和合",
                "业力果": "上爻成 = 业果成熟",
                "业力报": "变卦显 = 果报现前"
            },
            "types_of_karma": {
                "善业": "阳爻增多 → 吉卦",
                "恶业": "阴爻增多 → 凶卦",
                "无记业": "阴阳平衡 → 平卦",
                "不定业": "爻变不定 → 变数存"
            },
            "karma_wisdom": {
                "insight": "业力非宿命，可转化",
                "yao_bian_method": "通过爻变（修行）转化业力",
                "final_liberation": "超越业力，得大自在"
            }
        }
    
    def compare_impermanence(self):
        """
        对比无常与爻变
        """
        return {
            "buddhist_impermanence": "诸行无常，是生灭法",
            "yin_yang_impermanence": "阴阳消长，爻变不息",
            "hexagram_impermanence": "卦无常势，唯变所适",
            "comparison": {
                "conceptual": "无常 = 爻变（永恒变化）",
                "practical": "应对无常 = 观爻变而顺应",
                "liberation": "超越无常 = 悟阴阳本空"
            },
            "wisdom_application": [
                "观爻知变，预判趋势",
                "顺爻而动，不逆势而为",
                "超越爻变，安住本源"
            ]
        }
    
    def integrate_practice(self):
        """
        整合修行实践
        """
        return {
            "buddhist_practice": {
                "samatha": "止禅 → 定力",
                "vipassana": "观禅 → 智慧",
                "bodhi": "觉悟 → 解脱"
            },
            "yin_yang_practice": {
                "cultivate_yang": "培养阳德（善业）",
                "transform_yin": "转化阴霾（烦恼）",
                "balance_both": "阴阳调和（中道）"
            },
            "integrated_path": {
                "meditation": "静坐 → 观卦象变化",
                "wisdom": "观察 → 悟阴阳本空",
                "compassion": "行善 → 增长阳爻",
                "ethics": "持戒 → 避免阴爻"
            }
        }

def main():
    parser = argparse.ArgumentParser(description="佛学缘起与卦象映射")
    parser.add_argument("--twelve_links", action="store_true", help="十二因缘映射")
    parser.add_argument("--four_truths", action="store_true", help="四圣谛映射")
    parser.add_argument("--conditionality", action="store_true", help="缘起性空映射")
    parser.add_argument("--karma", action="store_true", help="业力映射")
    parser.add_argument("--impermanence", action="store_true", help="无常对比")
    parser.add_argument("--practice", action="store_true", help="修行实践整合")
    parser.add_argument("--all", action="store_true", help="完整映射")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    mapper = BuddhismMapper()
    
    if args.twelve_links:
        result = mapper.twelve_links_mapping
    elif args.four_truths:
        result = mapper.four_truths_mapping
    elif args.conditionality:
        result = mapper.map_conditionality()
    elif args.karma:
        result = mapper.map_karma()
    elif args.impermanence:
        result = mapper.compare_impermanence()
    elif args.practice:
        result = mapper.integrate_practice()
    elif args.all:
        result = {
            "twelve_links": mapper.twelve_links_mapping,
            "four_truths": mapper.four_truths_mapping,
            "conditionality": mapper.map_conditionality(),
            "karma": mapper.map_karma(),
            "impermanence": mapper.compare_impermanence(),
            "practice": mapper.integrate_practice()
        }
    else:
        # 默认：四圣谛映射
        result = mapper.four_truths_mapping
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【佛学与易经映射】")
        print("=" * 70)
        
        if "twelve_links" in result:
            print(f"\n【十二因缘映射】")
            for i, (link, mapping) in enumerate(result["twelve_links"].items(), 1):
                print(f"\n{i}. {link} → {mapping['gua']}")
                print(f"   含义：{mapping['meaning']}")
                print(f"   阴阳：{mapping['yin_yang']}")
                print(f"   佛学概念：{mapping['buddhist_concept']}")
        
        elif "conditionality" in result:
            cond = result["conditionality"]
            print(f"\n【缘起性空】")
            print(f"  核心教义：{cond['conditionality']}")
            print(f"\n  阴阳对应：")
            for key, value in cond["yin_yang_correspondence"].items():
                print(f"    {key}：{value}")
            print(f"\n  性空见：{cond['emptiness_insight']['concept']}")
            print(f"    阴阳解读：{cond['emptiness_insight']['yin_yang_interpretation']}")
        
        elif "karma_definition" in result:
            karma = result
            print(f"\n【业力映射】")
            print(f"  定义：{karma['karma_definition']}")
            print(f"\n  爻变对应：")
            for key, value in karma["yao_bian_correspondence"].items():
                print(f"    {key}：{value}")
            print(f"\n  业力智慧：{karma['karma_wisdom']['insight']}")
        
        elif "buddhist_impermanence" in result:
            imp = result
            print(f"\n【无常对比】")
            print(f"  佛学无常：{imp['buddhist_impermanence']}")
            print(f"  阴阳无常：{imp['yin_yang_impermanence']}")
            print(f"  卦象无常：{imp['hexagram_impermanence']}")
            print(f"\n  智慧应用：")
            for item in imp["wisdom_application"]:
                print(f"    • {item}")
        
        elif "buddhist_practice" in result:
            prac = result
            print(f"\n【修行实践整合】")
            print(f"\n  佛学修行：")
            for key, value in prac["buddhist_practice"].items():
                print(f"    {key}：{value}")
            print(f"\n  阴阳修行：")
            for key, value in prac["yin_yang_practice"].items():
                print(f"    {key}：{value}")
            print(f"\n  整合路径：")
            for key, value in prac["integrated_path"].items():
                print(f"    {key}：{value}")
        
        elif isinstance(result, dict) and "苦谛" in result:
            print(f"\n【四圣谛映射】")
            for truth, mapping in result.items():
                print(f"\n【{truth}】")
                print(f"  卦象：{mapping['gua']}")
                print(f"  阴阳：{mapping['yin_yang']}")
                print(f"  描述：{mapping['description']}")
                print(f"  关键点：")
                for point in mapping["key_points"]:
                    print(f"    • {point}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
