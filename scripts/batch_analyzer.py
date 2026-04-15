#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量分析工具
功能：多情景对比、多起卦方法对照
"""

import argparse
import json
import subprocess
import sys

def run_script(script_name, args):
    """
    运行脚本并返回结果
    """
    cmd = [sys.executable, f"/workspace/projects/i-ching-insight/scripts/{script_name}"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        return {"error": result.stderr}

def batch_divination(methods, scenarios):
    """
    批量起卦分析
    
    Args:
        methods: 起卦方法列表
        scenarios: 情景列表
    
    Returns:
        批量分析结果
    """
    results = {
        "method": "批量起卦分析",
        "scenarios": []
    }
    
    for scenario in scenarios:
        scenario_result = {
            "name": scenario.get("name", ""),
            "methods": []
        }
        
        for method in methods:
            if method == "coin":
                result = run_script("divination_helper.py", ["--method", "coin", "--format", "json"])
            elif method == "time":
                year = scenario.get("year")
                month = scenario.get("month")
                day = scenario.get("day")
                hour = scenario.get("hour")
                args = ["--method", "time", "--format", "json"]
                if year:
                    args.extend(["--year", str(year)])
                if month:
                    args.extend(["--month", str(month)])
                if day:
                    args.extend(["--day", str(day)])
                if hour:
                    args.extend(["--hour", str(hour)])
                result = run_script("divination_helper.py", args)
            elif method == "number":
                num1 = scenario.get("num1", 1)
                num2 = scenario.get("num2", 2)
                num3 = scenario.get("num3", 3)
                num4 = scenario.get("num4", 4)
                result = run_script("divination_helper.py", [
                    "--method", "number",
                    "--num1", str(num1),
                    "--num2", str(num2),
                    "--num3", str(num3),
                    "--num4", str(num4),
                    "--format", "json"
                ])
            else:
                result = {"error": f"未知方法：{method}"}
            
            scenario_result["methods"].append({
                "method": method,
                "result": result
            })
        
        results["scenarios"].append(scenario_result)
    
    return results

def compare_scenarios(results):
    """
    对比不同情景的结果
    """
    comparison = {
        "comparison_type": "情景对比",
        "summary": []
    }
    
    for scenario in results["scenarios"]:
        scenario_summary = {
            "name": scenario["name"],
            "methods_count": len(scenario["methods"]),
            "consistent": True,
            "hexagrams": []
        }
        
        first_hexagram = None
        
        for method_result in scenario["methods"]:
            if "error" not in method_result["result"]:
                hexagram = method_result["result"].get("hexagram_symbol", "")
                scenario_summary["hexagrams"].append({
                    "method": method_result["method"],
                    "hexagram": hexagram
                })
                
                if first_hexagram is None:
                    first_hexagram = hexagram
                elif hexagram != first_hexagram:
                    scenario_summary["consistent"] = False
        
        comparison["summary"].append(scenario_summary)
    
    return comparison

def main():
    parser = argparse.ArgumentParser(description="批量分析工具")
    parser.add_argument("--methods", help="起卦方法（逗号分隔）：coin,time,number")
    parser.add_argument("--scenario_file", help="情景文件（JSON格式）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 默认起卦方法
    if args.methods:
        methods = [m.strip() for m in args.methods.split(",")]
    else:
        methods = ["coin", "time", "number"]
    
    # 默认情景
    if args.scenario_file:
        with open(args.scenario_file, "r", encoding="utf-8") as f:
            scenarios = json.load(f)
    else:
        scenarios = [
            {
                "name": "情景1：当前时间",
                "year": 2024,
                "month": 4,
                "day": 15,
                "hour": 10,
                "num1": 8,
                "num2": 3,
                "num3": 15,
                "num4": 10
            },
            {
                "name": "情景2：特定时间",
                "year": 1990,
                "month": 5,
                "day": 20,
                "hour": 14,
                "num1": 5,
                "num2": 7,
                "num3": 9,
                "num4": 2
            }
        ]
    
    # 批量起卦
    results = batch_divination(methods, scenarios)
    
    # 情景对比
    comparison = compare_scenarios(results)
    
    final_result = {
        "batch_analysis": results,
        "comparison": comparison
    }
    
    # 输出
    if args.format == "json":
        print(json.dumps(final_result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【批量分析工具】")
        print("=" * 70)
        print(f"\n起卦方法：{', '.join(methods)}")
        print(f"情景数量：{len(scenarios)}")
        
        print("\n【情景分析】")
        for scenario in results["scenarios"]:
            print(f"\n{scenario['name']}:")
            for method_result in scenario["methods"]:
                if "error" not in method_result["result"]:
                    print(f"  {method_result['method']}: {method_result['result'].get('hexagram_symbol', '')}")
                else:
                    print(f"  {method_result['method']}: 错误")
        
        print("\n【情景对比】")
        for summary in comparison["summary"]:
            print(f"\n{summary['name']}:")
            print(f"  方法数：{summary['methods_count']}")
            print(f"  一致性：{'一致' if summary['consistent'] else '不一致'}")
            print(f"  卦象：")
            for hex_info in summary["hexagrams"]:
                print(f"    {hex_info['method']}: {hex_info['hexagram']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
