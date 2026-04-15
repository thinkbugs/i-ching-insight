#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
群论分析工具 - 揭示64卦的群结构
功能：证明64卦构成群，分析子群、商群、同态
"""

import argparse
import json
from itertools import product
import numpy as np

# 64卦列表（按二进制顺序）
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

class HexagramGroup:
    """
    六十四卦群（Z2^6群）
    """
    
    def __init__(self):
        self.elements = [i for i in range(64)]
        self.identity = 0  # 坤卦（全阴）作为单位元
        self.operation = self._xor  # 群运算定义为异或
        self.cayley_table = None
        self._build_cayley_table()
    
    def _xor(self, a, b):
        """群运算：异或"""
        return a ^ b
    
    def _build_cayley_table(self):
        """构建凯莱表（乘法表）"""
        n = len(self.elements)
        self.cayley_table = np.zeros((n, n), dtype=int)
        for i, a in enumerate(self.elements):
            for j, b in enumerate(self.elements):
                self.cayley_table[i][j] = self.operation(a, b)
    
    def verify_group_axioms(self):
        """
        验证群公理
        """
        n = len(self.elements)
        
        # 1. 封闭性
        closure = True
        for a in self.elements:
            for b in self.elements:
                if self.operation(a, b) not in self.elements:
                    closure = False
                    break
        
        # 2. 结合律
        associativity = True
        for a in self.elements:
            for b in self.elements:
                for c in self.elements:
                    if self.operation(a, self.operation(b, c)) != self.operation(self.operation(a, b), c):
                        associativity = False
                        break
                if not associativity:
                    break
            if not associativity:
                break
        
        # 3. 单位元
        identity_exists = True
        for a in self.elements:
            if self.operation(self.identity, a) != a or self.operation(a, self.identity) != a:
                identity_exists = False
                break
        
        # 4. 逆元
        inverse_exists = True
        for a in self.elements:
            found = False
            for b in self.elements:
                if self.operation(a, b) == self.identity and self.operation(b, a) == self.identity:
                    found = True
                    break
            if not found:
                inverse_exists = False
                break
        
        return {
            "closure": closure,
            "associativity": associativity,
            "identity": identity_exists,
            "inverse": inverse_exists,
            "is_group": closure and associativity and identity_exists and inverse_exists
        }
    
    def get_element_order(self, element):
        """
        计算元素的阶
        """
        if element == self.identity:
            return 1
        
        order = 1
        current = element
        while current != self.identity:
            current = self.operation(current, element)
            order += 1
            if order > 64:
                return None  # 防止无限循环
        
        return order
    
    def find_subgroups(self):
        """
        寻找所有子群
        """
        subgroups = []
        
        # 寻找所有可能的子集
        from itertools import combinations
        for size in [1, 2, 4, 8, 16, 32, 64]:
            for subset in combinations(self.elements, size):
                if 0 not in subset:
                    continue  # 必须包含单位元
                
                # 检查封闭性
                is_closed = True
                for a in subset:
                    for b in subset:
                        if self.operation(a, b) not in subset:
                            is_closed = False
                            break
                    if not is_closed:
                        break
                
                if is_closed:
                    subgroups.append(sorted(list(subset)))
        
        return subgroups
    
    def get_center(self):
        """
        计算群的中心（与所有元素可交换的元素集合）
        """
        center = []
        for a in self.elements:
            is_central = True
            for b in self.elements:
                if self.operation(a, b) != self.operation(b, a):
                    is_central = False
                    break
            if is_central:
                center.append(a)
        
        return center
    
    def get_conjugacy_classes(self):
        """
        计算共轭类
        """
        classes = []
        remaining = set(self.elements)
        
        while remaining:
            a = remaining.pop()
            conjugacy_class = set()
            
            for b in self.elements:
                # b * a * b^(-1) = b * a * b (因为是Z2群，每个元素是自己的逆元)
                conj = self.operation(self.operation(b, a), b)
                conjugacy_class.add(conj)
            
            classes.append(sorted(list(conjugacy_class)))
            remaining -= conjugacy_class
        
        return classes
    
    def analyze_structure(self):
        """
        分析群的代数结构
        """
        # 验证群公理
        axioms = self.verify_group_axioms()
        
        # 群的阶
        group_order = len(self.elements)
        
        # 元素的阶分布
        order_distribution = {}
        for element in self.elements:
            order = self.get_element_order(element)
            order_distribution[order] = order_distribution.get(order, 0) + 1
        
        # 群的中心
        center = self.get_center()
        
        # 共轭类
        conjugacy_classes = self.get_conjugacy_classes()
        
        # 子群（仅找主要子群）
        subgroups = self.find_subgroups()
        major_subgroups = [sg for sg in subgroups if len(sg) >= 8]
        
        return {
            "group_order": group_order,
            "axioms": axioms,
            "order_distribution": order_distribution,
            "center": center,
            "center_size": len(center),
            "conjugacy_classes": conjugacy_classes,
            "num_conjugacy_classes": len(conjugacy_classes),
            "major_subgroups": major_subgroups
        }

def analyze_gua_symmetries(gua_index):
    """
    分析特定卦象的对称性
    """
    # 将卦象索引转为6位二进制
    binary = bin(gua_index)[2:].zfill(6)
    
    # 计算错卦（阴阳全反）
    wrong_gua = 63 - gua_index  # 63 = 0b111111
    
    # 计算综卦（倒置）
    reversed_binary = binary[::-1]
    zong_gua = int(reversed_binary, 2)
    
    # 计算互卦（二三四爻为下卦，三四五爻为上卦）
    middle_4 = binary[1:5]
    if len(middle_4) < 4:
        middle_4 = middle_4.zfill(4)
    lower_trigram = int(middle_4[:2] + "0" * 4, 2)
    upper_trigram = int("0" * 4 + middle_4[2:], 2)
    hu_gua = (lower_trigram // 4) + (upper_trigram // 32) * 8
    
    return {
        "gua_index": gua_index,
        "gua_name": GUA_64[gua_index] if gua_index < 64 else "未知",
        "binary": binary,
        "wrong_gua_index": wrong_gua,
        "wrong_gua_name": GUA_64[wrong_gua],
        "zong_gua_index": zong_gua,
        "zong_gua_name": GUA_64[zong_gua],
        "hu_gua_index": hu_gua,
        "hu_gua_name": GUA_64[hu_gua] if hu_gua < 64 else "未知"
    }

def main():
    parser = argparse.ArgumentParser(description="群论分析工具")
    parser.add_argument("--verify", action="store_true", help="验证群公理")
    parser.add_argument("--analyze", action="store_true", help="分析群结构")
    parser.add_argument("--gua", type=int, help="分析特定卦象的对称性")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    group = HexagramGroup()
    
    if args.verify:
        result = group.verify_group_axioms()
    elif args.analyze:
        result = group.analyze_structure()
    elif args.gua is not None:
        result = analyze_gua_symmetries(args.gua)
    else:
        # 默认分析群结构
        result = group.analyze_structure()
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【六十四卦群论分析】")
        print("=" * 70)
        
        if "group_order" in result:
            print(f"\n【群基本信息】")
            print(f"  群的阶：{result['group_order']}")
            print(f"  群的类型：Z₂⁶（二进制六维向量群）")
            
            print(f"\n【群公理验证】")
            axioms = result["axioms"]
            print(f"  封闭性：{'✓' if axioms['closure'] else '✗'}")
            print(f"  结合律：{'✓' if axioms['associativity'] else '✗'}")
            print(f"  单位元：{'✓' if axioms['identity'] else '✗'}")
            print(f"  逆元：{'✓' if axioms['inverse'] else '✗'}")
            print(f"  是否为群：{'是 ✓' if axioms['is_group'] else '否 ✗'}")
            
            print(f"\n【元素的阶分布】")
            for order, count in sorted(result["order_distribution"].items()):
                print(f"  阶 {order}: {count} 个元素")
            
            print(f"\n【群的中心】")
            print(f"  大小：{result['center_size']}")
            print(f"  元素：{result['center']}")
            
            print(f"\n【共轭类】")
            print(f"  类数：{result['num_conjugacy_classes']}")
            for i, cls in enumerate(result["conjugacy_classes"][:5], 1):  # 只显示前5个
                print(f"  类 {i}: {cls[:10]}{'...' if len(cls) > 10 else ''}")
            
            print(f"\n【主要子群】")
            print(f"  数量：{len(result['major_subgroups'])}")
            for i, sg in enumerate(result['major_subgroups'][:3], 1):
                print(f"  子群 {i}: 大小 {len(sg)}")
        
        elif "gua_index" in result:
            print(f"\n【卦象对称性分析】")
            print(f"  卦名：{result['gua_name']}（{result['gua_index']}）")
            print(f"  二进制：{result['binary']}")
            print(f"\n  错卦：{result['wrong_gua_name']}（{result['wrong_gua_index']}）")
            print(f"  综卦：{result['zong_gua_name']}（{result['zong_gua_index']}）")
            print(f"  互卦：{result['hu_gua_name']}（{result['hu_gua_index']}）")
        
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
