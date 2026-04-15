#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例数据库脚本
功能：历史案例录入、查询、分析
"""

import argparse
import json

# 历史案例数据库
CASE_DATABASE = {
    "周文王演易": {
        "hexagram": "乾",
        "time": "商末周初",
        "method": "蓍草",
        "situation": "周文王被囚禁于羑里，推演易经",
        "question": "如何从困境中突破",
        "result": "演六十四卦，奠定周易基础",
        "outcome": "成功脱离困境，建立周朝",
        "key_points": [
            "乾卦象征天，代表刚健、进取",
            "从囚禁到突破，体现了天行健的精神",
            "通过演绎系统化知识，转化为行动力量"
        ]
    },
    "诸葛亮借东风": {
        "hexagram": "巽",
        "time": "三国时期",
        "method": "奇门",
        "situation": "赤壁之战前，急需东风",
        "question": "如何获得东风助力",
        "result": "成功借得东风，火攻曹营",
        "outcome": "赤壁大捷，三国鼎立",
        "key_points": [
            "巽为风，象征柔顺、渗透",
            "把握天时，顺应自然规律",
            "预测与行动相结合"
        ]
    },
    "刘伯温推演国运": {
        "hexagram": "坤",
        "time": "明朝建立前",
        "method": "奇门",
        "situation": "朱元璋问国运",
        "question": "明朝国运如何",
        "result": "预言大明三百年江山",
        "outcome": "明朝建立，延续近三百年",
        "key_points": [
            "坤为地，象征厚德载物",
            "把握历史大势，顺应民心",
            "系统推演，综合分析"
        ]
    },
    "王阳明悟道": {
        "hexagram": "复",
        "time": "明朝正德年间",
        "method": "内省",
        "situation": "被贬龙场，面临生死考验",
        "question": "何为心之本体",
        "result": "龙场悟道，创立心学",
        "outcome": "成为一代宗师，影响深远",
        "key_points": [
            "复卦象征回归、新生",
            "从困境中反思，找到内在力量",
            "知行合一，理论与实践结合"
        ]
    },
    "袁天罡李淳风预言": {
        "hexagram": "坎",
        "time": "唐朝",
        "method": "奇门",
        "situation": "推演历史走向",
        "question": "后世如何演变",
        "result": "《推背图》预言",
        "outcome": "预言应验，成为经典",
        "key_points": [
            "坎卦象征险陷，也象征智慧",
            "洞察历史规律，把握周期",
            "隐喻表达，留有解读空间"
        ]
    }
}

def query_case(case_name):
    """
    查询特定案例
    """
    case = CASE_DATABASE.get(case_name)
    if case:
        return {
            "case": case_name,
            "data": case
        }
    else:
        return {"error": f"未找到案例：{case_name}"}

def search_cases(keyword):
    """
    搜索案例
    """
    results = {
        "keyword": keyword,
        "matches": []
    }
    
    for case_name, case_data in CASE_DATABASE.items():
        # 在案例名称和内容中搜索
        if keyword in case_name or keyword in str(case_data):
            results["matches"].append({
                "name": case_name,
                "hexagram": case_data["hexagram"],
                "time": case_data["time"]
            })
    
    return results

def analyze_case_patterns():
    """
    分析案例模式
    """
    analysis = {
        "total_cases": len(CASE_DATABASE),
        "hexagram_distribution": {},
        "method_distribution": {},
        "success_rate": "高",
        "common_patterns": []
    }
    
    # 统计卦象分布
    for case_data in CASE_DATABASE.values():
        hexagram = case_data["hexagram"]
        analysis["hexagram_distribution"][hexagram] = analysis["hexagram_distribution"].get(hexagram, 0) + 1
        
        method = case_data["method"]
        analysis["method_distribution"][method] = analysis["method_distribution"].get(method, 0) + 1
    
    # 提取共同模式
    all_key_points = []
    for case_data in CASE_DATABASE.values():
        all_key_points.extend(case_data["key_points"])
    
    analysis["common_patterns"] = [
        "把握时机，顺应自然",
        "内外兼修，知行合一",
        "系统思维，整体把握",
        "变通灵活，因势利导"
    ]
    
    return analysis

def list_all_cases():
    """
    列出所有案例
    """
    cases = []
    for case_name, case_data in CASE_DATABASE.items():
        cases.append({
            "name": case_name,
            "hexagram": case_data["hexagram"],
            "time": case_data["time"],
            "method": case_data["method"]
        })
    
    return {
        "total": len(cases),
        "cases": cases
    }

def main():
    parser = argparse.ArgumentParser(description="案例数据库")
    parser.add_argument("--query", help="查询特定案例名称")
    parser.add_argument("--search", help="搜索关键词")
    parser.add_argument("--list", action="store_true", help="列出所有案例")
    parser.add_argument("--analyze", action="store_true", help="分析案例模式")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    result = None
    
    if args.query:
        result = query_case(args.query)
    elif args.search:
        result = search_cases(args.search)
    elif args.list:
        result = list_all_cases()
    elif args.analyze:
        result = analyze_case_patterns()
    else:
        # 默认列出所有案例
        result = list_all_cases()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "cases" in result:
            # 列表输出
            print("=" * 60)
            print("【历史案例数据库】")
            print("=" * 60)
            print(f"\n总案例数：{result['total']}")
            print("\n案例列表：")
            for i, case in enumerate(result["cases"], 1):
                print(f"\n{i}. {case['name']}")
                print(f"   卦象：{case['hexagram']}")
                print(f"   时间：{case['time']}")
                print(f"   方法：{case['method']}")
        
        elif "case" in result:
            # 案例详情输出
            case = result["data"]
            print("=" * 60)
            print(f"【{result['case']}】")
            print("=" * 60)
            print(f"\n卦象：{case['hexagram']}")
            print(f"时间：{case['time']}")
            print(f"方法：{case['method']}")
            print(f"\n情景：{case['situation']}")
            print(f"问题：{case['question']}")
            print(f"结果：{case['result']}")
            print(f"结局：{case['outcome']}")
            print(f"\n关键要点：")
            for point in case["key_points"]:
                print(f"  • {point}")
        
        elif "keyword" in result:
            # 搜索结果输出
            print("=" * 60)
            print(f"【搜索结果：{result['keyword']}】")
            print("=" * 60)
            print(f"\n匹配数：{len(result['matches'])}")
            print("\n匹配案例：")
            for match in result["matches"]:
                print(f"  • {match['name']}（{match['hexagram']}, {match['time']}）")
        
        elif "total_cases" in result:
            # 分析结果输出
            print("=" * 60)
            print("【案例模式分析】")
            print("=" * 60)
            print(f"\n总案例数：{result['total_cases']}")
            print(f"成功率：{result['success_rate']}")
            
            print(f"\n【卦象分布】")
            for hexagram, count in result["hexagram_distribution"].items():
                print(f"  {hexagram}: {count}次")
            
            print(f"\n【方法分布】")
            for method, count in result["method_distribution"].items():
                print(f"  {method}: {count}次")
            
            print(f"\n【共同模式】")
            for pattern in result["common_patterns"]:
                print(f"  • {pattern}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
