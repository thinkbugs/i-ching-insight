#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风水堪舆映射脚本
功能：八卦方位、二十四山、九星飞星
"""

import argparse
import json
import datetime

# 八卦方位
BAGUA_FANGWEI = {
    "乾": "西北", "坤": "西南", "震": "正东", "巽": "东南",
    "坎": "正北", "离": "正南", "艮": "东北", "兑": "正西"
}

# 二十四山
ERSHI_SI_SHAN = [
    "壬", "子", "癸",  # 北
    "丑", "艮", "寅",  # 东北
    "甲", "卯", "乙",  # 东
    "辰", "巽", "巳",  # 东南
    "丙", "午", "丁",  # 南
    "未", "坤", "申",  # 西南
    "庚", "酉", "辛",  # 西
    "戌", "乾", "亥"   # 西北
]

# 九星
JIU_XING_FEI_XING = [
    "贪狼", "巨门", "禄存", "文曲", "廉贞", "武曲", "破军", "左辅", "右弼"
]

# 九星吉凶
JIU_XING_JI_XIONG = {
    "贪狼": "吉", "巨门": "吉", "武曲": "吉", "左辅": "吉",
    "禄存": "凶", "文曲": "凶", "廉贞": "凶", "破军": "凶", "右弼": "平"
}

# 宅卦（根据坐向确定）
ZHAI_GUA = {
    "坎": "坎宅", "坤": "坤宅", "震": "震宅", "巽": "巽宅",
    "中": "中宫", "乾": "乾宅", "兑": "兑宅", "艮": "艮宅", "离": "离宅"
}

def get_zhai_gua(orientation):
    """根据朝向确定宅卦"""
    # 简化：根据朝向方位确定宅卦
    orientation_map = {
        "正北": "坎", "正南": "离", "正东": "震", "正西": "兑",
        "西北": "乾", "西南": "坤", "东北": "艮", "东南": "巽"
    }
    return orientation_map.get(orientation, "中")

def calculate_fei_xing(year=None):
    """计算九星飞星"""
    if year is None:
        year = datetime.datetime.now().year
    
    # 确定运（20年一运，2004-2023为八运）
    start_year = 2004
    yun = ((year - start_year) // 20) + 8
    if yun > 9:
        yun = yun % 9
    
    # 九星飞星（以运星为中心，按固定顺序排列）
    # 飞星顺序：4-9-2 / 3-5-7 / 8-1-6
    fei_xing_map = {
        4: 2, 9: 1, 2: 9,
        3: 3, 5: 5, 7: 7,
        8: 8, 1: 4, 6: 6
    }
    
    # 根据运星调整
    base_map = [2, 9, 4, 7, 5, 3, 8, 1, 6]
    shift = (yun - 5) % 9
    shifted_map = base_map[shift:] + base_map[:shift]
    
    fei_xing = {}
    for i, gong in enumerate([4, 9, 2, 3, 5, 7, 8, 1, 6]):
        fei_xing[gong] = JIU_XING_FEI_XING[shifted_map[i] - 1]
    
    return {
        "yun": yun,
        "yun_name": f"{yun}运",
        "fei_xing": fei_xing
    }

def analyze_fengshui(orientation=None, layout_type=None, year=None):
    """
    风水分析
    
    Args:
        orientation: 朝向（正北、正南等）
        layout_type: 户型类型（可选）
        year: 年份
    
    Returns:
        风水分析结果
    """
    result = {}
    
    # 宅卦
    if orientation:
        zhai_gua = get_zhai_gua(orientation)
        result["zhai_gua"] = {
            "orientation": orientation,
            "gua": zhai_gua,
            "name": ZHAI_GUA[zhai_gua]
        }
    
    # 九星飞星
    fei_xing_info = calculate_fei_xing(year)
    result["fei_xing"] = fei_xing_info
    
    # 方位分析
    fangwei_analysis = []
    for bagua, fangwei in BAGUA_FANGWEI.items():
        fangwei_analysis.append({
            "bagua": bagua,
            "fangwei": fangwei
        })
    result["fangwei"] = fangwei_analysis
    
    # 吉凶方位
    ji_fangwei = []
    xiong_fangwei = []
    
    for gong, xing in fei_xing_info["fei_xing"].items():
        jx = JIU_XING_JI_XIONG.get(xing, "平")
        if jx == "吉":
            ji_fangwei.append({"gong": gong, "xing": xing})
        elif jx == "凶":
            xiong_fangwei.append({"gong": gong, "xing": xing})
    
    result["ji_fangwei"] = ji_fangwei
    result["xiong_fangwei"] = xiong_fangwei
    
    # 建议
    suggestions = []
    
    if orientation:
        if result["zhai_gua"]["gua"] in ["坎", "离", "震", "巽"]:
            suggestions.append(f"{result['zhai_gua']['name']}为东四宅，宜东四命人居住")
        else:
            suggestions.append(f"{result['zhai_gua']['name']}为西四宅，宜西四命人居住")
    
    if ji_fangwei:
        suggestions.append(f"吉星方位：{', '.join([f'{j['gong']}宫{j['xing']}' for j in ji_fangwei[:3]])}")
    
    if xiong_fangwei:
        suggestions.append(f"凶星方位：{', '.join([f'{x['gong']}宫{x['xing']}' for x in xiong_fangwei[:3]])}，宜化解或避开")
    
    result["suggestions"] = suggestions
    
    return result

def main():
    parser = argparse.ArgumentParser(description="风水堪舆")
    parser.add_argument("--orientation", help="朝向（正北、正南、正东、正西、西北、西南、东北、东南）")
    parser.add_argument("--year", type=int, help="年份")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 风水分析
    result = analyze_fengshui(args.orientation, None, args.year)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【风水堪舆】")
        print("=" * 70)
        
        if result.get("zhai_gua"):
            print(f"\n【宅卦】")
            print(f"  朝向：{result['zhai_gua']['orientation']}")
            print(f"  宅卦：{result['zhai_gua']['name']}")
        
        print(f"\n【九星飞星】")
        print(f"  {result['fei_xing']['yun_name']}")
        for gong, xing in result['fei_xing']['fei_xing'].items():
            jx = JIU_XING_JI_XIONG.get(xing, "平")
            print(f"  {gong}宫：{xing}（{jx}）")
        
        if result.get("ji_fangwei"):
            print(f"\n【吉星方位】")
            for j in result['ji_fangwei']:
                print(f"  • {j['gong']}宫{j['jx']}")
        
        if result.get("xiong_fangwei"):
            print(f"\n【凶星方位】")
            for x in result['xiong_fangwei']:
                print(f"  • {x['gong']}宫{x['xing']}")
        
        if result.get("suggestions"):
            print(f"\n【建议】")
            for suggestion in result['suggestions']:
                print(f"  • {suggestion}")
        
        print("=" * 70)

if __name__ == "__main__":
    main()
