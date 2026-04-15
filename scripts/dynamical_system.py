#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动力系统分析工具 - 爻变的离散动力系统
功能：轨迹分析、周期轨道、混沌、Lyapunov指数
"""

import argparse
import json
import numpy as np
from collections import defaultdict

# 64卦列表
GUA_64 = [
    "坤", "剥", "比", "观", "豫", "晋", "萃", "否",
    "谦", "艮", "蹇", "渐", "小过", "旅", "咸", "遁",
    "师", "蒙", "坎", "涣", "解", "未济", "困", "讼",
    "升", "蛊", "井", "巽", "恒", "鼎", "大过", "姤",
    "复", "颐", "屯", "益", "震", "噬嗑", "随", "无妄",
    "明夷", "贲", "既济", "家人", "丰", "离", "革", "同人",
    "临", "损", "节", "中孚", "归妹", "睽", "兑", "履",
    "泰", "大畜", "需", "小畜", "大壮", "大有", "夬", "乾"
]

class HexagramDynamicalSystem:
    """
    卦象动力系统（离散动力系统）
    """
    
    def __init__(self):
        self.space_size = 64
        self.phase_space = list(range(64))
        self.trajectories = {}
    
    def _int_to_binary(self, n):
        """整数转6位二进制字符串"""
        return bin(n)[2:].zfill(6)
    
    def _binary_to_int(self, b):
        """二进制字符串转整数"""
        return int(b, 2)
    
    def apply_transition(self, state, moving_yao):
        """
        应用爻变（状态转移）
        moving_yao: 动爻位置列表（0-5，从初爻到上爻）
        """
        if not moving_yao:
            return state
        
        binary = list(self._int_to_binary(state))
        
        for yao in moving_yao:
            if 0 <= yao < 6:
                binary[yao] = '1' if binary[yao] == '0' else '0'
        
        return self._binary_to_int(''.join(binary))
    
    def simulate_trajectory(self, initial_state, transition_rules, max_steps=100):
        """
        模拟轨迹
        transition_rules: 状态转移规则函数或列表
        """
        trajectory = [initial_state]
        current = initial_state
        
        for step in range(max_steps):
            if callable(transition_rules):
                next_state = transition_rules(current, step)
            elif isinstance(transition_rules, list):
                # 使用预定义的转移规则
                rule_index = step % len(transition_rules)
                next_state = self.apply_transition(current, transition_rules[rule_index])
            else:
                break
            
            if next_state in trajectory:
                # 检测到周期
                cycle_start = trajectory.index(next_state)
                cycle = trajectory[cycle_start:]
                return {
                    "trajectory": trajectory + [next_state],
                    "is_periodic": True,
                    "period": len(cycle),
                    "cycle": cycle,
                    "transient_length": cycle_start
                }
            
            trajectory.append(next_state)
            current = next_state
            
            if current == initial_state:
                # 回到初始状态
                return {
                    "trajectory": trajectory,
                    "is_periodic": True,
                    "period": len(trajectory),
                    "cycle": trajectory,
                    "transient_length": 0
                }
        
        return {
            "trajectory": trajectory,
            "is_periodic": False,
            "period": None,
            "cycle": [],
            "transient_length": len(trajectory)
        }
    
    def find_fixed_points(self, transition_function):
        """
        寻找不动点（吸引子）
        """
        fixed_points = []
        
        for state in self.phase_space:
            next_state = transition_function(state)
            if next_state == state:
                fixed_points.append(state)
        
        return fixed_points
    
    def find_periodic_orbits(self, transition_function, max_period=10):
        """
        寻找周期轨道
        """
        periodic_orbits = defaultdict(list)
        
        for state in self.phase_space:
            trajectory = [state]
            current = state
            visited = {state: 0}
            
            for step in range(max_period * 2):
                next_state = transition_function(current)
                
                if next_state in visited:
                    cycle_length = step - visited[next_state]
                    if cycle_length <= max_period and cycle_length > 0:
                        periodic_orbits[cycle_length].append({
                            "orbit": trajectory[visited[next_state]:],
                            "start_state": next_state
                        })
                    break
                
                visited[next_state] = step + 1
                trajectory.append(next_state)
                current = next_state
        
        return dict(periodic_orbits)
    
    def calculate_basin_of_attraction(self, attractor, transition_function):
        """
        计算吸引域
        """
        basin = set()
        
        for state in self.phase_space:
            trajectory = [state]
            current = state
            
            for _ in range(100):
                if current == attractor:
                    basin.add(state)
                    break
                current = transition_function(current)
        
        return basin
    
    def analyze_lyapunov_exponent(self, initial_states, transition_function, max_steps=100):
        """
        计算Lyapunov指数（轨道发散速度）
        """
        # 对于离散系统，Lyapunov指数 ≈ (1/n) * ln(|f'(x)|)
        # 这里用数值方法估计
        
        # 选择两个初始状态（相差最小）
        if len(initial_states) < 2:
            initial_states = [0, 1]
        
        traj1 = self.simulate_trajectory(initial_states[0], transition_function, max_steps)["trajectory"]
        traj2 = self.simulate_trajectory(initial_states[1], transition_function, max_steps)["trajectory"]
        
        # 计算距离变化
        distances = []
        for i in range(min(len(traj1), len(traj2))):
            dist = self.hamming_distance(traj1[i], traj2[i])
            distances.append(dist)
        
        # 估计Lyapunov指数
        if len(distances) > 1:
            divergence_rate = []
            for i in range(1, len(distances)):
                if distances[i-1] > 0:
                    divergence_rate.append(np.log(distances[i] / distances[i-1]))
            
            lyapunov = np.mean(divergence_rate) if divergence_rate else 0.0
        else:
            lyapunov = 0.0
        
        return {
            "lyapunov_exponent": lyapunov,
            "chaotic": lyapunov > 0,  # Lyapunov指数 > 0 表示混沌
            "distance_evolution": distances[:20]
        }
    
    def hamming_distance(self, a, b):
        """汉明距离"""
        diff = a ^ b
        dist = 0
        while diff:
            dist += diff & 1
            diff >>= 1
        return dist
    
    def phase_portrait_analysis(self):
        """
        相图分析（状态空间的可视化参数）
        """
        # 计算状态空间的拓扑特性
        # 6-维超立方体的顶点
        
        # 计算每个状态的度数（相邻状态数）
        degrees = {}
        for state in self.phase_space:
            degrees[state] = 6  # 每个卦象有6个相邻卦象（变一爻）
        
        # 计算度数分布
        degree_distribution = defaultdict(int)
        for degree in degrees.values():
            degree_distribution[degree] += 1
        
        return {
            "phase_space_size": len(self.phase_space),
            "dimension": 6,
            "degree_distribution": dict(degree_distribution),
            "max_degree": max(degrees.values()),
            "min_degree": min(degrees.values()),
            "avg_degree": np.mean(list(degrees.values()))
        }
    
    def bifurcation_analysis(self, parameter_range, transition_function_factory):
        """
        分岔分析（参数变化对系统行为的影响）
        """
        bifurcation_data = []
        
        for param in parameter_range:
            transition_func = transition_function_factory(param)
            
            # 寻找不动点
            fixed_points = self.find_fixed_points(transition_func)
            
            # 寻找周期轨道
            periodic_orbits = self.find_periodic_orbits(transition_func, max_period=6)
            
            bifurcation_data.append({
                "parameter": param,
                "fixed_points": len(fixed_points),
                "periodic_orbits": {k: len(v) for k, v in periodic_orbits.items()}
            })
        
        return bifurcation_data

def sample_transition_rule_1(state, step):
    """
    示例转移规则1：每次变初爻
    """
    return state ^ 1  # 翻转最低位

def sample_transition_rule_2(state, step):
    """
    示例转移规则2：每次变上爻
    """
    return state ^ 32  # 翻转最高位

def sample_transition_rule_3(state, step):
    """
    示例转移规则3：每次变中间两爻
    """
    return state ^ 6  # 翻转第1、2位

def main():
    parser = argparse.ArgumentParser(description="动力系统分析工具")
    parser.add_argument("--trajectory", type=int, help="模拟轨迹（初始卦象）")
    parser.add_argument("--fixed", action="store_true", help="寻找不动点")
    parser.add_argument("--periodic", action="store_true", help="寻找周期轨道")
    parser.add_argument("--basin", type=int, help="计算吸引域（吸引子卦象）")
    parser.add_argument("--lyapunov", action="store_true", help="计算Lyapunov指数")
    parser.add_argument("--portrait", action="store_true", help="相图分析")
    parser.add_argument("--rule", type=int, choices=[1, 2, 3], default=1, help="转移规则")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    system = HexagramDynamicalSystem()
    
    # 选择转移规则
    rules = {
        1: sample_transition_rule_1,
        2: sample_transition_rule_2,
        3: sample_transition_rule_3
    }
    transition_func = rules[args.rule]
    
    if args.trajectory is not None:
        result = system.simulate_trajectory(args.trajectory, transition_func, max_steps=20)
    elif args.fixed:
        result = {
            "fixed_points": system.find_fixed_points(transition_func),
            "fixed_point_names": [GUA_64[i] for i in system.find_fixed_points(transition_func)]
        }
    elif args.periodic:
        orbits = system.find_periodic_orbits(transition_func, max_period=10)
        result = {
            "periodic_orbits": orbits
        }
    elif args.basin is not None:
        basin = system.calculate_basin_of_attraction(args.basin, transition_func)
        result = {
            "attractor": GUA_64[args.basin],
            "basin_size": len(basin),
            "basin_states": sorted(list(basin))
        }
    elif args.lyapunov:
        result = system.analyze_lyapunov_exponent([0, 1], transition_func, max_steps=50)
    elif args.portrait:
        result = system.phase_portrait_analysis()
    else:
        # 默认：相图分析
        result = system.phase_portrait_analysis()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【卦象动力系统分析】")
        print("=" * 70)
        
        if "trajectory" in result:
            traj = result["trajectory"]
            print(f"\n【轨迹模拟】")
            print(f"  初始状态：{GUA_64[traj[0]]}")
            print(f"  轨迹：{' → '.join([GUA_64[i] for i in traj[:10]])}")
            if result["is_periodic"]:
                print(f"  周期：{result['period']}")
                print(f"  周期轨道：{' → '.join([GUA_64[i] for i in result['cycle']])}")
                print(f"  暂态长度：{result['transient_length']}")
        
        elif "fixed_points" in result and "fixed_point_names" in result:
            print(f"\n【不动点分析】")
            print(f"  不动点数：{len(result['fixed_points'])}")
            print(f"  不动点：{', '.join(result['fixed_point_names'])}")
        
        elif "periodic_orbits" in result:
            print(f"\n【周期轨道分析】")
            for period, orbits in result["periodic_orbits"].items():
                print(f"  周期 {period}：{len(orbits)} 个轨道")
                for i, orbit in enumerate(orbits[:3], 1):
                    print(f"    轨道 {i}: {' → '.join([GUA_64[s] for s in orbit['orbit']])}")
        
        elif "basin_size" in result:
            print(f"\n【吸引域分析】")
            print(f"  吸引子：{result['attractor']}")
            print(f"  吸引域大小：{result['basin_size']}")
            print(f"  吸引域状态数：{len(result['basin_states'])}")
        
        elif "lyapunov_exponent" in result:
            print(f"\n【Lyapunov指数】")
            print(f"  Lyapunov指数：{result['lyapunov_exponent']:.6f}")
            print(f"  是否混沌：{'是' if result['chaotic'] else '否'}")
            print(f"  距离演化：{result['distance_evolution'][:10]}")
        
        elif "phase_space_size" in result:
            print(f"\n【相图分析】")
            print(f"  相空间大小：{result['phase_space_size']}")
            print(f"  维度：{result['dimension']}")
            print(f"  平均度数：{result['avg_degree']}")
            print(f"  度数分布：{result['degree_distribution']}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
