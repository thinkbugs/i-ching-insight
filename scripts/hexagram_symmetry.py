#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
64卦对称性分析脚本
功能：分析64卦的对称性（错卦、综卦、互卦）和卦序规律
"""

import argparse
import json

# 八卦对应
BAGUA_MAP = {
    0: ("坤", "☷"), 1: ("震", "☳"), 2: ("坎", "☵"), 3: ("兑", "☱"),
    4: ("艮", "☶"), 5: ("离", "☲"), 6: ("巽", "☴"), 7: ("乾", "☰")
}

# 64卦序列（按文王卦序）
HEXAGRAM_SEQUENCE = [
    ("乾", "☰☰"), ("坤", "☷☷"), ("屯", "☵☳"), ("蒙", "☳☵"), ("需", "☰☵"), ("讼", "☵☰"),
    ("师", "☵☷"), ("比", "☷☵"), ("小畜", "☴☰"), ("履", "☰☱"), ("泰", "☰☷"), ("否", "☷☰"),
    ("同人", "☰☲"), ("大有", "☲☰"), ("谦", "☶☷"), ("豫", "☷☶"), ("随", "☱☶"), ("蛊", "☶☴"),
    ("临", "☷☱"), ("观", "☴☷"), ("噬嗑", "☲☳"), ("贲", "☳☲"), ("剥", "☶☷"), ("复", "☷☳"),
    ("无妄", "☴☳"), ("大畜", "☶☰"), ("颐", "☶☳"), ("大过", "☴☱"), ("坎", "☵☵"), ("离", "☲☲"),
    ("咸", "☱☶"), ("恒", "☶☴"), ("遯", "☲☶"), ("大壮", "☳☰"), ("晋", "☲☷"), ("明夷", "☷☲"),
    ("家人", "☲☴"), ("睽", "☱☲"), ("蹇", "☶☵"), ("解", "☵☶"), ("损", "☱☶"), ("益", "☶☴"),
    ("夬", "☱☰"), ("姤", "☴☰"), ("萃", "☱☷"), ("升", "☷☴"), ("困", "☲☱"), ("井", "☴☶"),
    ("革", "☲☱"), ("鼎", "☲☴"), ("震", "☳☳"), ("艮", "☶☶"), ("渐", "☶☴"), ("归妹", "☱☳"),
    ("丰", "☲☳"), ("旅", "☳☲"), ("巽", "☴☴"), ("兑", "☱☱"), ("涣", "☴☵"), ("节", "☵☱"),
    ("中孚", "☴☱"), ("小过", "☳☶"), ("既济", "☵☲"), ("未济", "☲☵")
]

def symbol_to_binary(symbol):
    """将卦象符号转换为二进制"""
    # ☰=111, ☱=011, ☲=101, ☳=001, ☴=110, ☵=010, ☶=100, ☷=000
    symbol_map = {
        "☰": "111", "☱": "011", "☲": "101", "☳": "001",
        "☴": "110", "☵": "010", "☶": "100", "☷": "000"
    }
    
    upper = symbol_map[symbol[0]]
    lower = symbol_map[symbol[1]]
    return int(upper + lower, 2)

def binary_to_symbol(binary):
    """将二进制转换为卦象符号"""
    binary_str = f"{binary:06b}"
    
    symbol_map = {
        "111": "☰", "011": "☱", "101": "☲", "001": "☳",
        "110": "☴", "010": "☵", "100": "☶", "000": "☷"
    }
    
    upper = binary_str[:3]
    lower = binary_str[3:]
    return symbol_map[upper] + symbol_map[lower]

def get_cuo_gua(binary):
    """获取错卦（按位取反）"""
    return binary ^ 0b111111

def get_zong_gua(binary):
    """获取综卦（位序反转）"""
    binary_str = f"{binary:06b}"
    reversed_str = binary_str[::-1]
    return int(reversed_str, 2)

def get_hu_gua(binary):
    """获取互卦"""
    binary_str = f"{binary:06b}"
    # 下互：第2、3、4爻
    lower_hu = int(binary_str[1:4], 2)
    # 上互：第3、4、5爻
    upper_hu = int(binary_str[2:5], 2)
    # 互卦 = 上互 + 下互
    hu_binary = (upper_hu << 3) | lower_hu
    return hu_binary

def analyze_symmetry(hexagram_name=None):
    """
    分析64卦的对称性
    
    Args:
        hexagram_name: 特定卦名（可选）
    
    Returns:
        对称性分析结果
    """
    result = {
        "analysis_type": "64卦对称性分析",
        "hexagrams": []
    }
    
    if hexagram_name:
        # 分析特定卦
        for i, (name, symbol) in enumerate(HEXAGRAM_SEQUENCE):
            if name == hexagram_name:
                binary = symbol_to_binary(symbol)
                cuo_binary = get_cuo_gua(binary)
                zong_binary = get_zong_gua(binary)
                hu_binary = get_hu_gua(binary)
                
                # 查找卦名
                cuo_name = HEXAGRAM_SEQUENCE[cuo_binary][0]
                zong_name = HEXAGRAM_SEQUENCE[zong_binary][0]
                hu_name = HEXAGRAM_SEQUENCE[hu_binary][0]
                
                result["hexagrams"].append({
                    "name": name,
                    "symbol": symbol,
                    "binary": f"{binary:06b}",
                    "decimal": binary,
                    "cuo_gua": {
                        "name": cuo_name,
                        "symbol": HEXAGRAM_SEQUENCE[cuo_binary][1],
                        "binary": f"{cuo_binary:06b}",
                        "decimal": cuo_binary
                    },
                    "zong_gua": {
                        "name": zong_name,
                        "symbol": HEXAGRAM_SEQUENCE[zong_binary][1],
                        "binary": f"{zong_binary:06b}",
                        "decimal": zong_binary
                    },
                    "hu_gua": {
                        "name": hu_name,
                        "symbol": HEXAGRAM_SEQUENCE[hu_binary][1],
                        "binary": f"{hu_binary:06b}",
                        "decimal": hu_binary
                    },
                    "is_self_zong": (binary == zong_binary),
                    "is_self_cuo": (binary == cuo_binary)
                })
                break
    else:
        # 分析所有64卦
        cuo_pairs = []
        zong_pairs = []
        self_zong = []
        
        for i, (name, symbol) in enumerate(HEXAGRAM_SEQUENCE):
            binary = symbol_to_binary(symbol)
            cuo_binary = get_cuo_gua(binary)
            zong_binary = get_zong_gua(binary)
            hu_binary = get_hu_gua(binary)
            
            cuo_name = HEXAGRAM_SEQUENCE[cuo_binary][0]
            zong_name = HEXAGRAM_SEQUENCE[zong_binary][0]
            hu_name = HEXAGRAM_SEQUENCE[hu_binary][0]
            
            # 错卦对（避免重复）
            if i < cuo_binary:
                cuo_pairs.append({
                    "pair": [name, cuo_name],
                    "symbols": [symbol, HEXAGRAM_SEQUENCE[cuo_binary][1]]
                })
            
            # 综卦对（避免重复）
            if i < zong_binary:
                zong_pairs.append({
                    "pair": [name, zong_name],
                    "symbols": [symbol, HEXAGRAM_SEQUENCE[zong_binary][1]]
                })
            
            # 自综卦
            if binary == zong_binary:
                self_zong.append({
                    "name": name,
                    "symbol": symbol
                })
            
            result["hexagrams"].append({
                "sequence": i + 1,
                "name": name,
                "symbol": symbol,
                "binary": f"{binary:06b}",
                "decimal": binary,
                "cuo_gua": cuo_name,
                "zong_gua": zong_name,
                "hu_gua": hu_name
            })
        
        result["summary"] = {
            "total_hexagrams": 64,
            "cuo_pairs": len(cuo_pairs),
            "zong_pairs": len(zong_pairs),
            "self_zong_count": len(self_zong),
            "self_zong_hexagrams": self_zong
        }
    
    return result

def analyze_sequence_order():
    """
    分析卦序排列规律
    """
    result = {
        "analysis_type": "卦序排列规律",
        "sequence": []
    }
    
    for i, (name, symbol) in enumerate(HEXAGRAM_SEQUENCE):
        binary = symbol_to_binary(symbol)
        result["sequence"].append({
            "position": i + 1,
            "name": name,
            "symbol": symbol,
            "binary": f"{binary:06b}",
            "decimal": binary,
            "is_upper_even": (binary >> 3) % 2 == 0,
            "is_lower_even": (binary & 0b111) % 2 == 0
        })
    
    return result

def main():
    parser = argparse.ArgumentParser(description="64卦对称性分析")
    parser.add_argument("--hexagram", help="特定卦名（如：乾、坤、泰、否等）")
    parser.add_argument("--sequence", action="store_true", help="分析卦序排列规律")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 执行分析
    if args.sequence:
        result = analyze_sequence_order()
    else:
        result = analyze_symmetry(args.hexagram)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if args.hexagram:
            # 显示特定卦的对称性
            h = result["hexagrams"][0]
            print("=" * 70)
            print(f"【{h['name']}卦对称性分析】")
            print("=" * 70)
            print(f"\n卦象：{h['symbol']}")
            print(f"二进制：{h['binary']}")
            print(f"十进制：{h['decimal']}")
            
            print(f"\n【错卦】")
            print(f"  卦名：{h['cuo_gua']['name']}")
            print(f"  卦象：{h['cuo_gua']['symbol']}")
            print(f"  二进制：{h['cuo_gua']['binary']}")
            print(f"  十进制：{h['cuo_gua']['decimal']}")
            print(f"  说明：{'自错卦' if h['is_self_cuo'] else '错卦'}")
            
            print(f"\n【综卦】")
            print(f"  卦名：{h['zong_gua']['name']}")
            print(f"  卦象：{h['zong_gua']['symbol']}")
            print(f"  二进制：{h['zong_gua']['binary']}")
            print(f"  十进制：{h['zong_gua']['decimal']}")
            print(f"  说明：{'自综卦' if h['is_self_zong'] else '综卦'}")
            
            print(f"\n【互卦】")
            print(f"  卦名：{h['hu_gua']['name']}")
            print(f"  卦象：{h['hu_gua']['symbol']}")
            print(f"  二进制：{h['hu_gua']['binary']}")
            print(f"  十进制：{h['hu_gua']['decimal']}")
            
            print("=" * 70)
        else:
            # 显示整体对称性统计
            if result.get("summary"):
                print("=" * 70)
                print("【64卦对称性统计】")
                print("=" * 70)
                print(f"\n总卦数：{result['summary']['total_hexagrams']}")
                print(f"错卦对数：{result['summary']['cuo_pairs']}")
                print(f"综卦对数：{result['summary']['zong_pairs']}")
                print(f"自综卦数：{result['summary']['self_zong_count']}")
                
                if result['summary']['self_zong_hexagrams']:
                    print(f"\n自综卦：")
                    for h in result['summary']['self_zong_hexagrams']:
                        print(f"  • {h['name']} {h['symbol']}")
                
                print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
