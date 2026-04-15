#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字卦象映射脚本
功能：八字、命盘、流年流月卦象
"""

import argparse
import json
import datetime

# 八卦五行
BAGUA_WUXING = {
    "乾": "金", "兑": "金", "离": "火", "震": "木",
    "巽": "木", "坎": "水", "艮": "土", "坤": "土"
}

# 八卦符号
BAGUA_SYMBOL = {
    "乾": "☰", "兑": "☱", "离": "☲", "震": "☳",
    "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"
}

# 天干五行
TIAN_GAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行
DI_ZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def calculate_bazi(year, month, day, hour):
    """
    计算八字（简化版）
    """
    # 年干支
    year_gan = (year - 4) % 10
    year_zhi = (year - 4) % 12
    year_gan_zhi = TIAN_GAN[year_gan] + DI_ZHI[year_zhi]
    
    # 月干支（简化）
    month_gan = (year_gan * 2 + month) % 10
    month_zhi = (month + 2) % 12
    month_gan_zhi = TIAN_GAN[month_gan] + DI_ZHI[month_zhi]
    
    # 日干支（简化）
    base_date = datetime.date(1900, 1, 1)
    target_date = datetime.date(year, month, day)
    days_diff = (target_date - base_date).days
    day_gan = days_diff % 10
    day_zhi = days_diff % 12
    day_gan_zhi = TIAN_GAN[day_gan] + DI_ZHI[day_zhi]
    
    # 时干支（简化）
    shichen = (hour + 1) // 2 % 12
    shichen_zhi = DI_ZHI[shichen]
    shichen_gan = (day_gan * 2 + shichen) % 10
    shichen_gan_zhi = TIAN_GAN[shichen_gan] + shichen_zhi
    
    return {
        "year": year_gan_zhi,
        "month": month_gan_zhi,
        "day": day_gan_zhi,
        "hour": shichen_gan_zhi
    }

def bazi_to_gua(bazi):
    """
    八字转卦象（简化版）
    """
    # 年干 → 上卦
    year_gan = bazi["year"][0]
    year_gan_index = TIAN_GAN.index(year_gan)
    upper_gua_index = year_gan_index % 8
    upper_gua = list(BAGUA_SYMBOL.keys())[upper_gua_index]
    
    # 日支 → 下卦
    day_zhi = bazi["day"][1]
    day_zhi_index = DI_ZHI.index(day_zhi)
    lower_gua_index = day_zhi_index % 8
    lower_gua = list(BAGUA_SYMBOL.keys())[lower_gua_index]
    
    return {
        "upper": upper_gua,
        "lower": lower_gua,
        "symbol": BAGUA_SYMBOL[upper_gua] + BAGUA_SYMBOL[lower_gua],
        "name": upper_gua + lower_gua
    }

def calculate_liu_nian(bazi, current_year):
    """
    计算流年卦象
    """
    # 流年干支
    year_gan = (current_year - 4) % 10
    year_zhi = (current_year - 4) % 12
    year_gan_zhi = TIAN_GAN[year_gan] + DI_ZHI[year_zhi]
    
    # 流年卦象
    year_gan_index = TIAN_GAN.index(TIAN_GAN[year_gan])
    upper_gua_index = year_gan_index % 8
    upper_gua = list(BAGUA_SYMBOL.keys())[upper_gua_index]
    
    year_zhi_index = DI_ZHI.index(DI_ZHI[year_zhi])
    lower_gua_index = year_zhi_index % 8
    lower_gua = list(BAGUA_SYMBOL.keys())[lower_gua_index]
    
    return {
        "year": current_year,
        "gan_zhi": year_gan_zhi,
        "gua": upper_gua + lower_gua,
        "symbol": BAGUA_SYMBOL[upper_gua] + BAGUA_SYMBOL[lower_gua]
    }

def main():
    parser = argparse.ArgumentParser(description="八字卦象映射")
    parser.add_argument("--year", type=int, required=True, help="出生年份")
    parser.add_argument("--month", type=int, required=True, help="出生月份")
    parser.add_argument("--day", type=int, required=True, help="出生日期")
    parser.add_argument("--hour", type=int, required=True, help="出生时辰")
    parser.add_argument("--current_year", type=int, help="当前年份（用于流年分析）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 计算八字
    bazi = calculate_bazi(args.year, args.month, args.day, args.hour)
    
    # 八字转卦象
    ming_gua = bazi_to_gua(bazi)
    
    result = {
        "birth_time": f"{args.year}年{args.month}月{args.day}日{args.hour}时",
        "bazi": bazi,
        "ming_gua": ming_gua
    }
    
    # 流年分析
    if args.current_year:
        now = datetime.datetime.now()
        current_year = args.current_year or now.year
        liu_nian = calculate_liu_nian(bazi, current_year)
        result["liu_nian"] = liu_nian
    
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("【八字卦象映射】")
        print("=" * 60)
        print(f"\n出生时间：{result['birth_time']}")
        print(f"\n【八字】")
        print(f"  年柱：{bazi['year']}")
        print(f"  月柱：{bazi['month']}")
        print(f"  日柱：{bazi['day']}")
        print(f"  时柱：{bazi['hour']}")
        print(f"\n【本命卦】")
        print(f"  卦名：{ming_gua['name']}")
        print(f"  卦象：{ming_gua['symbol']}")
        print(f"  上卦：{ming_gua['upper']}（{BAGUA_WUXING[ming_gua['upper']]}）")
        print(f"  下卦：{ming_gua['lower']}（{BAGUA_WUXING[ming_gua['lower']]}）")
        
        if result.get("liu_nian"):
            print(f"\n【流年卦】")
            print(f"  年份：{result['liu_nian']['year']}")
            print(f"  干支：{result['liu_nian']['gan_zhi']}")
            print(f"  卦名：{result['liu_nian']['gua']}")
            print(f"  卦象：{result['liu_nian']['symbol']}")
        
        print("=" * 60)

if __name__ == "__main__":
    main()
