#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卦象可视化工具
功能：生成卦象的ASCII艺术图、五行分布图、结构分析图
"""

import argparse
import json

# 八卦符号
BAGUA_SYMBOL = {
    "乾": "☰", "兑": "☱", "离": "☲", "震": "☳",
    "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"
}

# 六十四卦名称
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

def gua_to_ascii(gua_name):
    """
    将卦象转换为ASCII艺术图
    """
    # 从卦名获取六十四卦索引
    if gua_name in GUA_64:
        index = GUA_64.index(gua_name)
    else:
        # 尝试解析（如"乾为天"）
        for i, name in enumerate(GUA_64):
            if gua_name.startswith(name):
                index = i
                break
        else:
            return None
    
    # 将索引转为二进制（6位）
    binary = bin(index)[2:].zfill(6)
    
    # 生成卦象ASCII图
    lines = []
    for bit in reversed(binary):  # 从上到下
        if bit == "1":
            lines.append("━━━━━")
        else:
            lines.append("━━━ ━━━")
    
    return lines

def visualize_hexagram(gua_name):
    """
    可视化卦象
    """
    ascii_gua = gua_to_ascii(gua_name)
    
    if ascii_gua is None:
        return None
    
    # 添加卦名和爻位
    yao_positions = ["上六", "六五", "六四", "六三", "六二", "初六"]
    
    lines = []
    lines.append(f"【{gua_name}】")
    lines.append("")
    
    for i, line in enumerate(ascii_gua):
        lines.append(f"{yao_positions[i]:4}  {line}")
    
    lines.append("")
    lines.append("━━━━━━━━━")
    lines.append("  阳  阴")
    
    return "\n".join(lines)

def visualize_wuxing_distribution(hexagram_data):
    """
    可视化五行分布
    """
    lines = []
    lines.append("【五行分布】")
    lines.append("")
    
    # 假设数据结构
    wuxing = hexagram_data.get("wuxing", {})
    
    # 简单的条形图
    elements = ["金", "木", "水", "火", "土"]
    for element in elements:
        count = wuxing.get(element, 0)
        bar = "█" * count
        lines.append(f"{element:2}  {bar:20} ({count})")
    
    return "\n".join(lines)

def visualize_structure(hexagram_data):
    """
    可视化卦象结构（上卦、下卦）
    """
    lines = []
    lines.append("【卦象结构】")
    lines.append("")
    
    upper = hexagram_data.get("upper_gua", "")
    lower = hexagram_data.get("lower_gua", "")
    
    if upper in BAGUA_SYMBOL and lower in BAGUA_SYMBOL:
        # 上卦
        lines.append(f"上卦：{upper}  {BAGUA_SYMBOL[upper]}")
        lines.append("")
        lines.append(gua_to_ascii(upper)[3])  # 上卦三爻
        
        # 下卦
        lines.append("")
        lines.append(f"下卦：{lower}  {BAGUA_SYMBOL[lower]}")
        lines.append("")
        lines.append(gua_to_ascii(lower)[3])  # 下卦三爻
        
        lines.append("")
        lines.append(f"完整卦象：{BAGUA_SYMBOL[upper]} {BAGUA_SYMBOL[lower]}")
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="卦象可视化工具")
    parser.add_argument("--gua", required=True, help="卦名（如"乾"、"乾为天"）")
    parser.add_argument("--type", default="ascii", 
                       choices=["ascii", "wuxing", "structure", "all"],
                       help="可视化类型")
    parser.add_argument("--data", help="额外数据（JSON格式）")
    
    args = parser.parse_args()
    
    # 读取额外数据
    extra_data = {}
    if args.data:
        try:
            import json
            extra_data = json.loads(args.data)
        except:
            pass
    
    result = {}
    
    if args.type in ["ascii", "all"]:
        ascii_viz = visualize_hexagram(args.gua)
        if ascii_viz:
            result["ascii"] = ascii_viz
    
    if args.type in ["wuxing", "all"]:
        if extra_data:
            wuxing_viz = visualize_wuxing_distribution(extra_data)
            result["wuxing"] = wuxing_viz
        else:
            result["wuxing"] = "需要提供--data参数"
    
    if args.type in ["structure", "all"]:
        if extra_data:
            structure_viz = visualize_structure(extra_data)
            result["structure"] = structure_viz
        else:
            result["structure"] = "需要提供--data参数"
    
    # 输出
    if args.type == "all":
        for key, value in result.items():
            print(value)
            print("\n")
    else:
        print(result.get(args.type, ""))

if __name__ == "__main__":
    main()
