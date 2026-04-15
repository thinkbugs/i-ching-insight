#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卦象心理学映射脚本
功能：将易经卦象映射到现代心理学概念
"""

import argparse
import json

# 心理学概念映射
PSYCHOLOGY_MAPPING = {
    "乾": {
        "type": "阳刚型人格",
        "traits": ["自信", "进取", "领导力", "目标导向"],
        "strengths": ["决断力强", "执行力强", "抗压能力强"],
        "weaknesses": ["可能过于强势", "缺乏灵活性", "忽视他人感受"],
        "development": ["培养同理心", "学会倾听", "平衡刚柔"]
    },
    "坤": {
        "type": "阴柔型人格",
        "traits": ["包容", "耐心", "协作", "支持性"],
        "strengths": ["适应性强", "团队协作好", "耐心细致"],
        "weaknesses": ["缺乏主动性", "依赖性强", "决策困难"],
        "development": ["培养独立思考", "提升领导力", "明确边界"]
    },
    "震": {
        "type": "激发型人格",
        "traits": ["冲动", "创新", "变革", "冒险"],
        "strengths": ["创造力强", "行动力强", "突破常规"],
        "weaknesses": ["缺乏持久性", "容易冲动", "计划不足"],
        "development": ["培养耐心", "加强规划", "学习反思"]
    },
    "巽": {
        "type": "渗透型人格",
        "traits": ["灵活", "适应", "沟通", "影响力"],
        "strengths": ["适应性强", "沟通能力强", "善于协调"],
        "weaknesses": ["缺乏坚定立场", "容易摇摆", "难以坚持"],
        "development": ["建立核心原则", "提升决断力", "明确目标"]
    },
    "坎": {
        "type": "深沉型人格",
        "traits": ["深刻", "洞察", "坚韧", "隐忍"],
        "strengths": ["洞察力强", "意志坚定", "适应困难"],
        "weaknesses": ["容易悲观", "缺乏开放性", "社交困难"],
        "development": ["培养乐观", "增加开放性", "主动交流"]
    },
    "离": {
        "type": "明亮型人格",
        "traits": ["热情", "表达", "社交", "感染力"],
        "strengths": ["表达能力强", "社交能力强", "有感染力"],
        "weaknesses": ["可能浮躁", "缺乏深度", "容易耗竭"],
        "development": ["培养深度", "注重内涵", "学会独处"]
    },
    "艮": {
        "type": "稳定型人格",
        "traits": ["稳重", "保守", "谨慎", "坚持"],
        "strengths": ["稳定性强", "执行力强", "风险意识强"],
        "weaknesses": ["缺乏灵活性", "过于保守", "变革困难"],
        "development": ["增强灵活性", "接受变革", "勇于尝试"]
    },
    "兑": {
        "type": "交流型人格",
        "traits": ["表达", "交流", "愉悦", "互动"],
        "strengths": ["沟通能力强", "社交能力好", "善于表达"],
        "weaknesses": ["缺乏深度", "容易表面化", "难以坚持"],
        "development": ["培养深度", "注重内涵", "坚持原则"]
    }
}

# 现代心理学概念
MODERN_PSYCHOLOGY = {
    "自我实现": ["乾", "离"],
    "情绪调节": ["坎", "艮"],
    "人际关系": ["坤", "兑"],
    "创造力": ["震", "巽"],
    "适应能力": ["巽", "坤"],
    "领导力": ["乾", "震"]
}

def analyze_hexagram_psychology(gua_name):
    """
    分析卦象的心理学意义
    """
    # 提取主要卦名
    main_gua = None
    for gua in PSYCHOLOGY_MAPPING.keys():
        if gua_name.startswith(gua):
            main_gua = gua
            break
    
    if not main_gua:
        return {"error": f"未找到卦象 {gua_name} 的心理学映射"}
    
    mapping = PSYCHOLOGY_MAPPING[main_gua]
    
    # 找出相关的现代心理学概念
    related_concepts = []
    for concept, guas in MODERN_PSYCHOLOGY.items():
        if main_gua in guas:
            related_concepts.append(concept)
    
    result = {
        "hexagram": gua_name,
        "main_gua": main_gua,
        "personality_type": mapping["type"],
        "personality_traits": mapping["traits"],
        "strengths": mapping["strengths"],
        "weaknesses": mapping["weaknesses"],
        "development_suggestions": mapping["development"],
        "related_psychology_concepts": related_concepts
    }
    
    return result

def compare_hexagrams_psychology(gua_list):
    """
    对比多个卦象的心理学特征
    """
    results = {
        "comparison_type": "心理学对比",
        "hexagrams": []
    }
    
    for gua in gua_list:
        analysis = analyze_hexagram_psychology(gua)
        results["hexagrams"].append(analysis)
    
    # 找出共同点和差异
    all_traits = []
    for analysis in results["hexagrams"]:
        all_traits.extend(analysis.get("personality_traits", []))
    
    common_traits = []
    unique_traits = {}
    
    for trait in set(all_traits):
        count = all_traits.count(trait)
        if count == len(gua_list):
            common_traits.append(trait)
        else:
            for i, analysis in enumerate(results["hexagrams"]):
                if trait in analysis.get("personality_traits", []):
                    if gua_list[i] not in unique_traits:
                        unique_traits[gua_list[i]] = []
                    unique_traits[gua_list[i]].append(trait)
    
    results["summary"] = {
        "common_traits": common_traits,
        "unique_traits": unique_traits
    }
    
    return results

def main():
    parser = argparse.ArgumentParser(description="卦象心理学映射")
    parser.add_argument("--gua", help="卦名（如"乾"、"乾为天"）")
    parser.add_argument("--compare", help="对比多个卦象（逗号分隔）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    result = None
    
    if args.compare:
        # 对比模式
        gua_list = [g.strip() for g in args.compare.split(",")]
        result = compare_hexagrams_psychology(gua_list)
    elif args.gua:
        # 单卦分析
        result = analyze_hexagram_psychology(args.gua)
    else:
        print("请使用 --gua 或 --compare 参数")
        return
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "comparison_type" in result:
            # 对比模式输出
            print("=" * 60)
            print("【卦象心理学对比】")
            print("=" * 60)
            
            for hex_data in result["hexagrams"]:
                print(f"\n【{hex_data['hexagram']}】")
                print(f"人格类型：{hex_data['personality_type']}")
                print(f"人格特质：{', '.join(hex_data['personality_traits'])}")
            
            print(f"\n【对比摘要】")
            print(f"共同特质：{', '.join(result['summary']['common_traits'])}")
            print(f"独特特质：")
            for gua, traits in result["summary"]["unique_traits"].items():
                print(f"  {gua}: {', '.join(traits)}")
        else:
            # 单卦分析输出
            print("=" * 60)
            print("【卦象心理学分析】")
            print("=" * 60)
            print(f"\n卦象：{result['hexagram']}")
            print(f"主卦：{result['main_gua']}")
            print(f"\n人格类型：{result['personality_type']}")
            print(f"\n人格特质：")
            for trait in result["personality_traits"]:
                print(f"  • {trait}")
            print(f"\n优势：")
            for strength in result["strengths"]:
                print(f"  • {strength}")
            print(f"\n不足：")
            for weakness in result["weaknesses"]:
                print(f"  • {weakness}")
            print(f"\n发展建议：")
            for suggestion in result["development_suggestions"]:
                print(f"  • {suggestion}")
            print(f"\n相关心理学概念：{', '.join(result['related_psychology_concepts'])}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
