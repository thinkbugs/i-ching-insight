#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准确性分析工具
功能：验证预测准确性、对比不同方法
"""

import argparse
import json
import random
from datetime import datetime

# 预测记录数据库
PREDICTION_RECORDS = []

# 六十四卦列表
GUA_64 = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济"
]

def add_prediction_record(gua, method, question, outcome, accuracy_score):
    """
    添加预测记录
    """
    record = {
        "id": len(PREDICTION_RECORDS) + 1,
        "timestamp": datetime.now().isoformat(),
        "gua": gua,
        "method": method,
        "question": question,
        "outcome": outcome,
        "accuracy_score": accuracy_score,
        "correct": accuracy_score >= 7  # 7分以上视为正确
    }
    PREDICTION_RECORDS.append(record)
    return record

def calculate_overall_accuracy():
    """
    计算整体准确性
    """
    if not PREDICTION_RECORDS:
        return {"error": "暂无预测记录"}
    
    total = len(PREDICTION_RECORDS)
    correct = sum(1 for r in PREDICTION_RECORDS if r["correct"])
    
    accuracy_rate = correct / total * 100
    average_score = sum(r["accuracy_score"] for r in PREDICTION_RECORDS) / total
    
    return {
        "total_predictions": total,
        "correct_predictions": correct,
        "accuracy_rate": round(accuracy_rate, 2),
        "average_score": round(average_score, 2)
    }

def analyze_method_accuracy():
    """
    分析不同方法的准确性
    """
    if not PREDICTION_RECORDS:
        return {"error": "暂无预测记录"}
    
    method_stats = {}
    
    for record in PREDICTION_RECORDS:
        method = record["method"]
        if method not in method_stats:
            method_stats[method] = {
                "total": 0,
                "correct": 0,
                "total_score": 0
            }
        
        method_stats[method]["total"] += 1
        if record["correct"]:
            method_stats[method]["correct"] += 1
        method_stats[method]["total_score"] += record["accuracy_score"]
    
    results = {}
    for method, stats in method_stats.items():
        accuracy = stats["correct"] / stats["total"] * 100
        avg_score = stats["total_score"] / stats["total"]
        results[method] = {
            "total": stats["total"],
            "correct": stats["correct"],
            "accuracy_rate": round(accuracy, 2),
            "average_score": round(avg_score, 2)
        }
    
    return {"method_analysis": results}

def analyze_hexagram_accuracy():
    """
    分析不同卦象的准确性
    """
    if not PREDICTION_RECORDS:
        return {"error": "暂无预测记录"}
    
    gua_stats = {}
    
    for record in PREDICTION_RECORDS:
        gua = record["gua"]
        if gua not in gua_stats:
            gua_stats[gua] = {
                "total": 0,
                "correct": 0,
                "total_score": 0
            }
        
        gua_stats[gua]["total"] += 1
        if record["correct"]:
            gua_stats[gua]["correct"] += 1
        gua_stats[gua]["total_score"] += record["accuracy_score"]
    
    results = {}
    for gua, stats in gua_stats.items():
        accuracy = stats["correct"] / stats["total"] * 100
        avg_score = stats["total_score"] / stats["total"]
        results[gua] = {
            "total": stats["total"],
            "accuracy_rate": round(accuracy, 2),
            "average_score": round(avg_score, 2)
        }
    
    return {"hexagram_analysis": results}

def generate_sample_data(n=20):
    """
    生成示例数据（用于演示）
    """
    methods = ["coin", "time", "number"]
    outcomes = ["应验", "部分应验", "未应验"]
    questions = [
        "事业发展", "感情问题", "健康运势", "财运", "学业",
        "投资决策", "合作机会", "人际关系", "家庭事务", "出行安全"
    ]
    
    for i in range(n):
        gua = random.choice(GUA_64)
        method = random.choice(methods)
        question = random.choice(questions)
        outcome = random.choice(outcomes)
        
        # 根据结果分配分数
        if outcome == "应验":
            score = random.randint(8, 10)
        elif outcome == "部分应验":
            score = random.randint(5, 7)
        else:
            score = random.randint(0, 4)
        
        add_prediction_record(gua, method, question, outcome, score)

def export_records():
    """
    导出预测记录
    """
    return {
        "export_time": datetime.now().isoformat(),
        "total_records": len(PREDICTION_RECORDS),
        "records": PREDICTION_RECORDS
    }

def main():
    parser = argparse.ArgumentParser(description="准确性分析工具")
    parser.add_argument("--overall", action="store_true", help="显示整体准确性")
    parser.add_argument("--method", action="store_true", help="分析不同方法的准确性")
    parser.add_argument("--hexagram", action="store_true", help="分析不同卦象的准确性")
    parser.add_argument("--add", help="添加预测记录（JSON格式）")
    parser.add_argument("--generate", type=int, help="生成示例数据（指定数量）")
    parser.add_argument("--export", action="store_true", help="导出所有记录")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    result = None
    
    if args.generate:
        generate_sample_data(args.generate)
        result = {"status": "success", "message": f"已生成 {args.generate} 条示例数据"}
    
    elif args.add:
        try:
            data = json.loads(args.add)
            record = add_prediction_record(
                data["gua"],
                data["method"],
                data["question"],
                data["outcome"],
                data["accuracy_score"]
            )
            result = {"status": "success", "record": record}
        except Exception as e:
            result = {"error": f"数据格式错误：{str(e)}"}
    
    elif args.overall:
        result = calculate_overall_accuracy()
    
    elif args.method:
        result = analyze_method_accuracy()
    
    elif args.hexagram:
        result = analyze_hexagram_accuracy()
    
    elif args.export:
        result = export_records()
    
    else:
        # 默认显示整体准确性
        result = calculate_overall_accuracy()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if "total_predictions" in result:
            # 整体准确性输出
            print("=" * 60)
            print("【整体准确性分析】")
            print("=" * 60)
            print(f"\n总预测数：{result['total_predictions']}")
            print(f"正确预测数：{result['correct_predictions']}")
            print(f"准确率：{result['accuracy_rate']}%")
            print(f"平均得分：{result['average_score']}/10")
        
        elif "method_analysis" in result:
            # 方法分析输出
            print("=" * 60)
            print("【起卦方法准确性对比】")
            print("=" * 60)
            for method, stats in result["method_analysis"].items():
                print(f"\n【{method}】")
                print(f"  预测数：{stats['total']}")
                print(f"  正确数：{stats['correct']}")
                print(f"  准确率：{stats['accuracy_rate']}%")
                print(f"  平均得分：{stats['average_score']}/10")
        
        elif "hexagram_analysis" in result:
            # 卦象分析输出
            print("=" * 60)
            print("【卦象准确性分析】")
            print("=" * 60)
            for gua, stats in result["hexagram_analysis"].items():
                print(f"\n【{gua}】")
                print(f"  预测数：{stats['total']}")
                print(f"  准确率：{stats['accuracy_rate']}%")
                print(f"  平均得分：{stats['average_score']}/10")
        
        elif "total_records" in result:
            # 导出输出
            print("=" * 60)
            print("【预测记录导出】")
            print("=" * 60)
            print(f"\n导出时间：{result['export_time']}")
            print(f"总记录数：{result['total_records']}")
            print("\n记录列表：")
            for record in result["records"]:
                print(f"\nID: {record['id']}")
                print(f"  时间：{record['timestamp']}")
                print(f"  卦象：{record['gua']}")
                print(f"  方法：{record['method']}")
                print(f"  问题：{record['question']}")
                print(f"  结果：{record['outcome']}")
                print(f"  得分：{record['accuracy_score']}/10")
        
        elif "status" in result:
            print(result["message"])
        
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
