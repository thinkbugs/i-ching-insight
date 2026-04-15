#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规则进化器 - 爻变规则的自我优化
功能：遗传算法、适应度评估、规则变异
"""

import argparse
import json
import random
import numpy as np

class RuleEvolver:
    """
    规则进化器
    """
    
    def __init__(self):
        self.rules = []
        self.generation = 0
    
    def initialize_population(self, population_size=10):
        """
        初始化规则种群
        """
        self.rules = []
        for _ in range(population_size):
            # 随机生成爻变规则
            rule = {
                "id": _,
                "yao_weights": [random.random() for _ in range(6)],
                "threshold": random.random(),
                "fitness": 0.0
            }
            self.rules.append(rule)
        self.generation = 1
    
    def evaluate_fitness(self, rule, environment_feedback):
        """
        评估适应度
        """
        # 简化适应度：根据反馈计算
        fitness = sum(environment_feedback) / len(environment_feedback) if environment_feedback else 0.5
        
        rule["fitness"] = fitness
        return fitness
    
    def select_parents(self, n_parents=2):
        """
        选择父代（轮盘赌选择）
        """
        total_fitness = sum(rule["fitness"] for rule in self.rules)
        if total_fitness == 0:
            return random.sample(self.rules, n_parents)
        
        parents = []
        for _ in range(n_parents):
            r = random.uniform(0, total_fitness)
            cumulative = 0
            for rule in self.rules:
                cumulative += rule["fitness"]
                if cumulative >= r:
                    parents.append(rule)
                    break
        
        return parents
    
    def crossover(self, parent1, parent2):
        """
        交叉（产生子代）
        """
        # 单点交叉
        crossover_point = random.randint(1, 5)
        
        child_weights = (
            parent1["yao_weights"][:crossover_point] +
            parent2["yao_weights"][crossover_point:]
        )
        
        child = {
            "id": f"gen{self.generation}_child",
            "yao_weights": child_weights,
            "threshold": (parent1["threshold"] + parent2["threshold"]) / 2,
            "fitness": 0.0
        }
        
        return child
    
    def mutate(self, rule, mutation_rate=0.1):
        """
        变异
        """
        for i in range(len(rule["yao_weights"])):
            if random.random() < mutation_rate:
                rule["yao_weights"][i] = random.random()
        
        if random.random() < mutation_rate:
            rule["threshold"] = random.random()
        
        return rule
    
    def evolve(self, environment_feedback):
        """
        进化一代
        """
        # 评估适应度
        for rule in self.rules:
            self.evaluate_fitness(rule, environment_feedback)
        
        # 选择父代
        parents = self.select_parents(2)
        
        # 交叉产生子代
        child = self.crossover(parents[0], parents[1])
        
        # 变异
        child = self.mutate(child)
        
        # 更新种群（保留最佳，替换最差）
        self.rules.sort(key=lambda x: x["fitness"], reverse=True)
        self.rules[-1] = child
        
        self.generation += 1
        
        return {
            "generation": self.generation,
            "best_fitness": self.rules[0]["fitness"],
            "average_fitness": sum(r["fitness"] for r in self.rules) / len(self.rules),
            "best_rule": self.rules[0]
        }
    
    def get_best_rule(self):
        """
        获取最佳规则
        """
        if not self.rules:
            return None
        return max(self.rules, key=lambda x: x["fitness"])

def main():
    parser = argparse.ArgumentParser(description="规则进化器")
    parser.add_argument("--initialize", type=int, help="初始化种群（种群大小）")
    parser.add_argument("--evolve", action="store_true", help="进化一代")
    parser.add_argument("--generations", type=int, help="进化多代")
    parser.add_argument("--best", action="store_true", help="获取最佳规则")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    evolver = RuleEvolver()
    
    if args.initialize:
        evolver.initialize_population(args.initialize)
        result = {"status": "initialized", "population_size": args.initialize}
    elif args.evolve or args.generations:
        if not evolver.rules:
            evolver.initialize_population(10)
        
        generations = args.generations if args.generations else 1
        
        # 模拟环境反馈
        for _ in range(generations):
            feedback = [random.random() for _ in range(10)]
            result = evolver.evolve(feedback)
        
    elif args.best:
        result = evolver.get_best_rule() if evolver.rules else {"error": "No rules"}
    else:
        # 默认：初始化并进化
        evolver.initialize_population(10)
        feedback = [random.random() for _ in range(10)]
        result = evolver.evolve(feedback)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【规则进化器】")
        print("=" * 70)
        
        if "generation" in result:
            print(f"\n【进化结果】")
            print(f"  代数：{result['generation']}")
            print(f"  最佳适应度：{result['best_fitness']:.4f}")
            print(f"  平均适应度：{result['average_fitness']:.4f}")
            print(f"  最佳规则：{result['best_rule']['id']}")
        
        elif "best_rule" in result:
            print(f"\n【最佳规则】")
            rule = result
            print(f"  规则ID：{rule['id']}")
            print(f"  适应度：{rule['fitness']:.4f}")
            print(f"  爻变权重：{[f'{w:.2f}' for w in rule['yao_weights']]}")
        
        elif "status" in result:
            print(f"\n【初始化】")
            print(f"  状态：{result['status']}")
            print(f"  种群大小：{result['population_size']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
