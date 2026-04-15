#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元认知模块 - 自我反思与优化
功能：评估自身决策、自我修正、元学习
"""

import argparse
import json

class MetaCognition:
    """
    元认知模块
    """
    
    def __init__(self):
        self.decision_history = []
        self.performance_metrics = {}
    
    def record_decision(self, decision, outcome, confidence):
        """
        记录决策
        """
        record = {
            "decision": decision,
            "outcome": outcome,
            "confidence": confidence,
            "accuracy": 1 if outcome == "success" else 0
        }
        self.decision_history.append(record)
    
    def evaluate_performance(self):
        """
        评估性能
        """
        if not self.decision_history:
            return {"error": "无决策记录"}
        
        total = len(self.decision_history)
        correct = sum(r["accuracy"] for r in self.decision_history)
        accuracy = correct / total
        
        avg_confidence = sum(r["confidence"] for r in self.decision_history) / total
        
        self.performance_metrics = {
            "total_decisions": total,
            "correct_decisions": correct,
            "accuracy": accuracy,
            "average_confidence": avg_confidence
        }
        
        return self.performance_metrics
    
    def self_reflection(self):
        """
        自我反思
        """
        if not self.decision_history:
            return {"error": "无决策记录"}
        
        # 分析决策模式
        high_confidence_errors = [
            r for r in self.decision_history
            if r["confidence"] > 0.7 and r["accuracy"] == 0
        ]
        
        low_confidence_success = [
            r for r in self.decision_history
            if r["confidence"] < 0.3 and r["accuracy"] == 1
        ]
        
        reflection = {
            "strengths": [],
            "weaknesses": [],
            "improvements": []
        }
        
        if len(high_confidence_errors) > len(self.decision_history) * 0.2:
            reflection["weaknesses"].append("过度自信")
            reflection["improvements"].append("校准置信度")
        
        if accuracy := sum(r["accuracy"] for r in self.decision_history) / len(self.decision_history) < 0.6:
            reflection["weaknesses"].append("准确率偏低")
            reflection["improvements"].append("优化决策模型")
        
        return reflection
    
    def self_correction(self, error_type):
        """
        自我修正
        """
        corrections = {
            "过度自信": "降低预测阈值，增加不确定性",
            "准确率偏低": "重新训练模型，调整参数",
            "偏见": "平衡训练数据，去偏见化"
        }
        
        correction = corrections.get(error_type, "未知错误类型")
        
        return {
            "error_type": error_type,
            "correction": correction,
            "status": "已识别，待应用"
        }
    
    def meta_learning(self, task_performance):
        """
        元学习
        """
        # 分析不同任务的表现
        task_analysis = {}
        
        for task, metrics in task_performance.items():
            task_analysis[task] = {
                "performance": metrics["accuracy"],
                "learning_speed": metrics["speed"],
                "generalization": metrics["generalization"]
            }
        
        # 学习策略
        strategy = {
            "focus_on_weak_tasks": [task for task, analysis in task_analysis.items()
                                   if analysis["performance"] < 0.6],
            "maintain_strength_tasks": [task for task, analysis in task_analysis.items()
                                      if analysis["performance"] > 0.8],
            "adaptive_learning": True
        }
        
        return {
            "task_analysis": task_analysis,
            "learning_strategy": strategy
        }

def main():
    parser = argparse.ArgumentParser(description="元认知模块")
    parser.add_argument("--record", nargs=3, help="记录决策（决策 结果 置信度）")
    parser.add_argument("--evaluate", action="store_true", help="评估性能")
    parser.add_argument("--reflect", action="store_true", help="自我反思")
    parser.add_argument("--correct", type=str, help="自我修正")
    parser.add_argument("--meta_learn", type=str, help="元学习（JSON格式）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    meta = MetaCognition()
    
    if args.record and len(args.record) == 3:
        meta.record_decision(args.record[0], args.record[1], float(args.record[2]))
        result = {"status": "recorded"}
    elif args.evaluate:
        result = meta.evaluate_performance()
    elif args.reflect:
        result = meta.self_reflection()
    elif args.correct:
        result = meta.self_correction(args.correct)
    elif args.meta_learn:
        try:
            task_perf = json.loads(args.meta_learn)
            result = meta.meta_learning(task_perf)
        except:
            result = {"error": "JSON格式错误"}
    else:
        # 默认：评估性能
        meta.record_decision("decision1", "success", 0.8)
        meta.record_decision("decision2", "failure", 0.7)
        meta.record_decision("decision3", "success", 0.9)
        result = meta.evaluate_performance()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【元认知模块】")
        print("=" * 70)
        
        if "total_decisions" in result:
            print(f"\n【性能评估】")
            print(f"  总决策数：{result['total_decisions']}")
            print(f"  正确决策数：{result['correct_decisions']}")
            print(f"  准确率：{result['accuracy']:.2f}")
            print(f"  平均置信度：{result['average_confidence']:.2f}")
        
        elif "strengths" in result:
            print(f"\n【自我反思】")
            print(f"  优势：{result['strengths']}")
            print(f"  劣势：{result['weaknesses']}")
            print(f"  改进：{result['improvements']}")
        
        elif "correction" in result:
            print(f"\n【自我修正】")
            print(f"  错误类型：{result['error_type']}")
            print(f"  修正方案：{result['correction']}")
            print(f"  状态：{result['status']}")
        
        elif "learning_strategy" in result:
            print(f"\n【元学习】")
            print(f"  学习策略：{result['learning_strategy']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
