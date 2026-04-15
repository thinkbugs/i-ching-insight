#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动爻推演脚本
功能：模拟多动爻组合、爻变规律、本卦→互卦→之卦→变卦的完整路径
"""

import argparse
import json

# 阴阳爻
YIN = 0
YANG = 1

# 八卦映射
TRIGRAM_MAP = {
    "000": ("坤", "☷"),
    "001": ("震", "☳"),
    "010": ("坎", "☵"),
    "011": ("兑", "☱"),
    "100": ("艮", "☶"),
    "101": ("离", "☲"),
    "110": ("巽", "☴"),
    "111": ("乾", "☰")
}

# 64卦映射（按易经顺序）
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

def yao_to_hexagram(yao_list):
    """
    将爻列表转换为卦象
    """
    binary_str = "".join(map(str, yao_list))
    
    # 查找64卦
    for i, (name, symbol) in enumerate(HEXAGRAM_SEQUENCE):
        # 需要将符号转换为二进制
        # ☰=111, ☱=011, ☲=101, ☳=001, ☴=110, ☵=010, ☶=100, ☷=000
        symbol_to_binary = {
            "☰": "111", "☱": "011", "☲": "101", "☳": "001",
            "☴": "110", "☵": "010", "☶": "100", "☷": "000"
        }
        
        actual_binary = symbol_to_binary[symbol[:1]] + symbol_to_binary[symbol[1:]]
        if actual_binary == binary_str:
            return {
                "name": name,
                "symbol": symbol,
                "binary": binary_str,
                "sequence": i + 1,
                "type": "本卦"
            }
    
    # 如果找不到，返回自定义
    return {
        "name": "未知卦",
        "symbol": binary_str,
        "binary": binary_str,
        "sequence": 0,
        "type": "本卦"
    }

def get_hu_gua(yao_list):
    """
    获取互卦（取本卦的2,3,4爻为下互，3,4,5爻为上互）
    """
    # 下互：2,3,4爻（索引1,2,3）
    lower_hu = yao_list[1:4]
    # 上互：3,4,5爻（索引2,3,4）
    upper_hu = yao_list[2:5]
    
    lower_hu_info = yao_to_hexagram(lower_hu)
    upper_hu_info = yao_to_hexagram(upper_hu)
    
    # 互卦 = 上互 + 下互
    hu_yao = upper_hu + lower_hu
    hu_info = yao_to_hexagram(hu_yao)
    
    return {
        "hu_gua": hu_info,
        "lower_hu": lower_hu_info,
        "upper_hu": upper_hu_info
    }

def get_cuo_gua(yao_list):
    """
    获取错卦（阴阳全反）
    """
    cuo_yao = [1 - y for y in yao_list]
    return yao_to_hexagram(cuo_yao)

def get_zong_gua(yao_list):
    """
    获取综卦（上下反转）
    """
    zong_yao = yao_list[::-1]
    return yao_to_hexagram(zong_yao)

def get_zhi_gua(yao_list, moving_positions):
    """
    获取之卦（根据动爻变化）
    
    Args:
        yao_list: 原始六爻
        moving_positions: 动爻位置列表（0-5）
    
    Returns:
        之卦信息
    """
    zhi_yao = yao_list.copy()
    changed_positions = []
    
    for pos in moving_positions:
        if 0 <= pos < 6:
            zhi_yao[pos] = 1 - zhi_yao[pos]  # 阴阳翻转
            changed_positions.append(pos)
    
    zhi_info = yao_to_hexagram(zhi_yao)
    zhi_info["changed_positions"] = changed_positions
    zhi_info["type"] = "之卦"
    
    return zhi_info

def simulate_dongyao(yao_list, moving_positions):
    """
    模拟动爻推演
    
    Args:
        yao_list: 原始六爻
        moving_positions: 动爻位置列表（0-5）
    
    Returns:
        完整的推演路径
    """
    if len(moving_positions) == 0:
        return {"error": "没有动爻"}
    
    result = {
        "original_yao": yao_list,
        "moving_positions": moving_positions,
        "moving_count": len(moving_positions),
        "path": []
    }
    
    # 1. 本卦
    ben_gua = yao_to_hexagram(yao_list)
    result["ben_gua"] = ben_gua
    result["path"].append(ben_gua)
    
    # 2. 互卦
    hu_gua_info = get_hu_gua(yao_list)
    result["hu_gua"] = hu_gua_info
    result["path"].append({
        "name": f"{hu_gua_info['upper_hu']['name']}（上互）+{hu_gua_info['lower_hu']['name']}（下互）",
        "type": "互卦",
        "description": f"本卦{ben_gua['name']}的互卦是{hu_gua_info['hu_gua']['name']}"
    })
    
    # 3. 之卦
    zhi_gua_info = get_zhi_gua(yao_list, moving_positions)
    result["zhi_gua"] = zhi_gua_info
    result["path"].append(zhi_gua_info)
    
    # 4. 错卦
    cuo_gua_info = get_cuo_gua(yao_list)
    result["cuo_gua"] = cuo_gua_info
    result["path"].append(cuo_gua_info)
    
    # 5. 综卦
    zong_gua_info = get_zong_gua(yao_list)
    result["zong_gua"] = zong_gua_info
    result["path"].append(zong_gua_info)
    
    # 6. 之卦的互卦
    if zhi_gua_info.get("binary"):
        zhi_hu_gua_info = get_hu_gua([int(c) for c in zhi_gua_info["binary"]])
        result["zhi_hu_gua"] = zhi_hu_gua_info
        result["path"].append({
            "name": f"{zhi_hu_gua_info['hu_gua']['name']}",
            "type": "之卦之互",
            "description": f"之卦{zhi_gua_info['name']}的互卦是{zhi_hu_gua_info['hu_gua']['name']}"
        })
    
    # 动爻分析
    result["dongyao_analysis"] = analyze_dongyao(yao_list, moving_positions, ben_gua, zhi_gua_info)
    
    return result

def analyze_dongyao(yao_list, moving_positions, ben_gua, zhi_gua_info):
    """
    分析动爻的变化
    """
    analysis = []
    
    yao_position_names = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]
    yao_type_names = ["阴爻", "阳爻"]
    
    for pos in moving_positions:
        if 0 <= pos < 6:
            original_yao = yao_list[pos]
            original_type = yao_type_names[original_yao]
            changed_type = yao_type_names[1 - original_yao]
            
            analysis.append({
                "position": yao_position_names[pos],
                "original": original_type,
                "changed": changed_type,
                "change_type": f"{original_type}变{changed_type}",
                "meaning": f"本卦{ben_gua['name']}之{yao_position_names[pos]}{original_type}，变为{zhi_gua_info['name']}之{yao_position_names[pos]}{changed_type}"
            })
    
    return analysis

def moving_list(yao_list):
    """
    获取动爻列表
    """
    return [i for i, y in enumerate(yao_list) if y == -1]

def main():
    parser = argparse.ArgumentParser(description="动爻推演")
    parser.add_argument("--yao", required=True, help="六爻列表，用逗号分隔（0=阴，1=阳），例如：0,0,1,0,1,1")
    parser.add_argument("--moving", required=True, help="动爻位置列表，用逗号分隔（0-5），例如：0,2")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 解析爻列表
    try:
        yao_list = [int(y.strip()) for y in args.yao.split(",")]
        if len(yao_list) != 6:
            raise ValueError("必须提供6个爻")
        if any(y not in [0, 1] for y in yao_list):
            raise ValueError("爻值必须是0或1")
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return
    
    # 解析动爻位置
    try:
        moving_positions = [int(m.strip()) for m in args.moving.split(",")]
        if any(m not in range(6) for m in moving_positions):
            raise ValueError("动爻位置必须是0-5")
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return
    
    # 模拟动爻推演
    result = simulate_dongyao(yao_list, moving_positions)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        print("=" * 70)
        print(f"本卦：{result['ben_gua']['name']} {result['ben_gua']['symbol']}")
        print(f"动爻：{', '.join(['初二三四五上'[i] + '爻' for i in result['moving_positions']])}")
        print("=" * 70)
        print("\n【卦变路径】\n")
        
        for i, step in enumerate(result["path"], 1):
            print(f"{i}. {step['type']}: {step.get('name', step.get('symbol', ''))}")
            if step.get("description"):
                print(f"   {step['description']}")
            print()
        
        print("=" * 70)
        print("【动爻变化】\n")
        
        for dongyao in result["dongyao_analysis"]:
            print(f"{dongyao['position']}: {dongyao['change_type']}")
            print(f"  {dongyao['meaning']}")
            print()
        
        print("=" * 70)
        print(f"推演说明：")
        print(f"• 本卦→互卦→之卦：爻变的基本路径")
        print(f"• 错卦：阴阳全反，体现对立统一")
        print(f"• 综卦：上下反转，体现相对视角")
        print("=" * 70)

if __name__ == "__main__":
    main()
