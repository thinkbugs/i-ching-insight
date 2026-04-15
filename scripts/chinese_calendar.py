#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国日历计算脚本
功能：农历转换、节气计算、干支纪年
"""

import argparse
import json
import datetime

# 天干
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# 生肖
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
# 节气
JIE_QI = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分",
    "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分",
    "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

def calculate_gan_zhi(year, month, day):
    """
    计算干支（简化版）
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
    
    return {
        "year": year_gan_zhi,
        "month": month_gan_zhi,
        "day": day_gan_zhi,
        "sheng_xiao": SHENG_XIAO[year_zhi]
    }

def calculate_jie_qi(year, month):
    """
    计算节气（简化版，近似日期）
    """
    # 节气日期（近似）
    jie_qi_dates = [
        (1, 6), (1, 20), (2, 4), (2, 19), (3, 6), (3, 21),
        (4, 5), (4, 20), (5, 6), (5, 21), (6, 6), (6, 21),
        (7, 7), (7, 23), (8, 8), (8, 23), (9, 8), (9, 23),
        (10, 8), (10, 23), (11, 7), (11, 22), (12, 7), (12, 22)
    ]
    
    current_jie_qi = None
    next_jie_qi = None
    
    for i, (jm, jd) in enumerate(jie_qi_dates):
        if jm == month:
            current_jie_qi = JIE_QI[i]
            if i < 23:
                next_jm, next_jd = jie_qi_dates[i + 1]
                if next_jm == month:
                    next_jie_qi = JIE_QI[i + 1]
                else:
                    next_jie_qi = JIE_QI[i + 1]
            break
    
    return {
        "current": current_jie_qi,
        "next": next_jie_qi
    }

def convert_to_lunar(year, month, day):
    """
    公历转农历（简化版）
    """
    # 简化：农历月份 ≈ 公历月份
    # 精确转换需要复杂算法，这里使用简化版本
    lunar_year = year
    lunar_month = month
    lunar_day = day
    
    # 简单调整
    if month in [1, 2]:
        lunar_year = year - 1
    elif month == 3 and day < 21:
        lunar_year = year - 1
    
    return {
        "year": lunar_year,
        "month": lunar_month,
        "day": lunar_day
    }

def main():
    parser = argparse.ArgumentParser(description="中国日历计算")
    parser.add_argument("--year", type=int, help="年份")
    parser.add_argument("--month", type=int, help="月份")
    parser.add_argument("--day", type=int, help="日期")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    if args.year is None:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
    else:
        year = args.year
        month = args.month or 1
        day = args.day or 1
    
    # 计算干支
    gan_zhi = calculate_gan_zhi(year, month, day)
    
    # 计算节气
    jie_qi = calculate_jie_qi(year, month)
    
    # 转换农历
    lunar = convert_to_lunar(year, month, day)
    
    result = {
        "gregorian": f"{year}年{month}月{day}日",
        "lunar": f"{lunar['year']}年{lunar['month']}月{lunar['day']}日",
        "gan_zhi": gan_zhi,
        "jie_qi": jie_qi
    }
    
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("【中国日历】")
        print("=" * 60)
        print(f"\n公历：{result['gregorian']}")
        print(f"农历：{result['lunar']}")
        print(f"\n【干支纪年】")
        print(f"  年干支：{gan_zhi['year']}（{gan_zhi['sheng_xiao']}）")
        print(f"  月干支：{gan_zhi['month']}")
        print(f"  日干支：{gan_zhi['day']}")
        print(f"\n【节气】")
        print(f"  当前节气：{jie_qi['current'] or '无'}")
        print(f"  下个节气：{jie_qi['next'] or '无'}")
        print("=" * 60)

if __name__ == "__main__":
    main()
