#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
紫微斗数卦象映射脚本
功能：十二宫、星辰与卦象对应
"""

import argparse
import json

# 十二宫
SHI_ER_GONG = [
    "命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄",
    "迁移", "仆役", "官禄", "田宅", "福德", "父母"
]

# 十四主星
SHI_SI_ZHU_XING = [
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
    "天府", "太阴", "贪狼", "巨门", "天相", "天梁",
    "七杀", "破军"
]

# 星辰五行
XING_WUXING = {
    "紫微": "土", "天机": "木", "太阳": "火", "武曲": "金",
    "天同": "水", "廉贞": "火", "天府": "土", "太阴": "水",
    "贪狼": "木", "巨门": "土", "天相": "水", "天梁": "土",
    "七杀": "金", "破军": "水"
}

# 卦象映射（星辰到卦象）
XING_TO_GUA = {
    "紫微": "乾", "天机": "巽", "太阳": "离", "武曲": "兑",
    "天同": "坎", "廉贞": "离", "天府": "坤", "太阴": "坎",
    "贪狼": "震", "巨门": "坤", "天相": "坎", "天梁": "艮",
    "七杀": "兑", "破军": "坎"
}

def calculate_ming_gan_zhi(year, month, day, hour):
    """
    计算命盘干支（简化版）
    """
    # 简化：使用年月日时生成命盘
    
    # 命宫位置（简化：根据时辰确定）
    shichen = (hour + 1) // 2 % 12
    ming_gong_index = shichen
    
    return ming_gong_index

def distribute_stars(ming_gong_index, year, month, day):
    """
    分配星辰（简化版）
    """
    # 简化：根据年月日随机分配星辰到十二宫
    import random
    
    ming_pan = {}
    stars_to_distribute = SHI_SI_ZHU_XING.copy()
    random.seed(year * 10000 + month * 100 + day)
    random.shuffle(stars_to_distribute)
    
    for i, gong in enumerate(SHI_ER_GONG):
        gong_index = (ming_gong_index + i) % 12
        # 每宫分配1-2颗星辰
        if stars_to_distribute:
            star = stars_to_distribute.pop(0)
            ming_pan[gong] = {
                "name": gong,
                "star": star,
                "wuxing": XING_WUXING.get(star, ""),
                "gua": XING_TO_GUA.get(star, "")
            }
        else:
            ming_pan[gong] = {
                "name": gong,
                "star": "",
                "wuxing": "",
                "gua": ""
            }
    
    return ming_pan

def analyze_ziwei(year, month, day, hour):
    """
    紫微斗数分析
    
    Args:
        year/month/day/hour: 出生时间
    
    Returns:
        紫微斗数命盘分析
    """
    result = {
        "birth_time": f"{year}年{month}月{day}日{hour}时"
    }
    
    # 计算命宫
    ming_gong_index = calculate_ming_gan_zhi(year, month, day, hour)
    result["ming_gong"] = {
        "name": SHI_ER_GONG[ming_gong_index],
        "index": ming_gong_index + 1
    }
    
    # 分配星辰
    ming_pan = distribute_stars(ming_gong_index, year, month, day)
    result["ming_pan"] = ming_pan
    
    # 命宫分析
    ming_gong_info = ming_pan[SHI_ER_GONG[ming_gong_index]]
    result["ming_gong_analysis"] = {
        "star": ming_gong_info["star"],
        "wuxing": ming_gong_info["wuxing"],
        "gua": ming_gong_info["gua"],
        "description": f"命宫主星为{ming_gong_info['star']}，五行属{ming_gong_info['wuxing']}，对应{ming_gong_info['gua']}卦"
    }
    
    # 五行统计
    wuxing_count = {}
    for gong_info in ming_pan.values():
        wuxing = gong_info["wuxing"]
        if wuxing:
            wuxing_count[wuxing] = wuxing_count.get(wuxing, 0) + 1
    
    result["wuxing_analysis"] = wuxing_count
    
    # 卦象统计
    gua_count = {}
    for gong_info in ming_pan.values():
        gua = gong_info["gua"]
        if gua:
            gua_count[gua] = gua_count.get(gua, 0) + 1
    
    result["gua_analysis"] = gua_count
    
    # 关键领域分析
    key_areas = {
        "命宫": ming_pan.get("命宫", {}),
        "财帛": ming_pan.get("财帛", {}),
        "官禄": ming_pan.get("官禄", {}),
        "夫妻": ming_pan.get("夫妻", {}),
        "福德": ming_pan.get("福德", {})
    }
    
    result["key_areas"] = key_areas
    
    return result

def main():
    parser = argparse.ArgumentParser(description="紫微斗数卦象映射")
    parser.add_argument("--year", type=int, required=True, help="出生年份")
    parser.add_argument("--month", type=int, required=True, help="出生月份")
    parser.add_argument("--day", type=int, required=True, help="出生日期")
    parser.add_argument("--hour", type=int, required=True, help="出生时辰")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 分析紫微斗数
    result = analyze_ziwei(args.year, args.month, args.day, args.hour)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print(f"【紫微斗数】{result['birth_time']}")
        print("=" * 70)
        
        print(f"\n【命宫】")
        print(f"  位置：{result['ming_gong']['name']}")
        print(f"  {result['ming_gong_analysis']['description']}")
        
        print(f"\n【命盘】")
        for gong in SHI_ER_GONG:
            info = result["ming_pan"][gong]
            if info["star"]:
                print(f"  {gong}：{info['star']}（{info['wuxing']}） → {info['gua']}卦")
        
        if result.get("wuxing_analysis"):
            print(f"\n【五行分布】")
            for wuxing, count in result['wuxing_analysis'].items():
                print(f"  {wuxing}：{count}个")
        
        if result.get("gua_analysis"):
            print(f"\n【卦象分布】")
            for gua, count in result['gua_analysis'].items():
                print(f"  {gua}卦：{count}个")
        
        if result.get("key_areas"):
            print(f"\n【关键领域】")
            for area, info in result['key_areas'].items():
                if info.get("star"):
                    print(f"  {area}：{info['star']}（{info['gua']}卦）")
        
        print("=" * 70)

if __name__ == "__main__":
    main()
