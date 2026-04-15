#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
梅花易数计算脚本
功能：体用互变、上互下互、外应内应、卦数推演
"""

import argparse
import json
import datetime

# 八卦数理
BAGUA_NUM = {
    "乾": 1, "兑": 2, "离": 3, "震": 4,
    "巽": 5, "坎": 6, "艮": 7, "坤": 8
}

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

# 互卦映射（上下互）
HU_GUA_MAP = {
    "乾": {"上": "乾", "下": "乾"},
    "兑": {"上": "巽", "下": "坎"},
    "离": {"上": "坎", "下": "巽"},
    "震": {"上": "坤", "下": "艮"},
    "巽": {"上": "艮", "下": "坤"},
    "坎": {"上": "离", "下": "兑"},
    "艮": {"上": "震", "下": "巽"},
    "坤": {"上": "乾", "下": "乾"}
}

def num_to_gua(num):
    """数字转八卦"""
    return list(BAGUA_NUM.keys())[num % 8 - 1]

def wuxing_sheng_ke(wuxing1, wuxing2):
    """五行生克判断"""
    sheng = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    ke = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
    
    if sheng.get(wuxing1) == wuxing2:
        return "生", f"{wuxing1}生{wuxing2}"
    elif ke.get(wuxing1) == wuxing2:
        return "克", f"{wuxing1}克{wuxing2}"
    elif sheng.get(wuxing2) == wuxing1:
        return "被生", f"{wuxing2}生{wuxing1}"
    elif ke.get(wuxing2) == wuxing1:
        return "被克", f"{wuxing2}克{wuxing1}"
    else:
        return "和", "五行相同"

def calculate_plum_blossom(year=None, month=None, day=None, hour=None, num1=None, num2=None, num3=None, num4=None):
    """
    梅花易数计算
    
    Args:
        year/month/day/hour: 时间卦参数
        num1/num2/num3/num4: 数字卦参数（年+月+日、时、起卦数、应卦数）
    
    Returns:
        梅花易数分析结果
    """
    result = {}
    
    if num1 is not None:
        # 数字卦模式
        result["method"] = "数字卦"
        result["input"] = f"{num1}, {num2}, {num3}, {num4}"
        
        # 上卦 = num1 + num2 + num3
        upper_num = (num1 + num2 + num3) % 8
        upper_gua = num_to_gua(upper_num)
        
        # 下卦 = num1 + num2 + num3 + num4
        lower_num = (num1 + num2 + num3 + num4) % 8
        lower_gua = num_to_gua(lower_num)
        
        # 动爻 = num1 + num2 + num3 + num4
        dongyao = (num1 + num2 + num3 + num4) % 6
        
    else:
        # 时间卦模式
        result["method"] = "时间卦"
        now = datetime.datetime.now() if year is None else datetime.datetime(year, month or 1, day or 1, hour or 0)
        
        year_num = (now.year - 1900) % 100
        month_num = now.month
        day_num = now.day
        hour_num = (now.hour + 1) // 2
        
        result["input"] = f"{now.year}年{now.month}月{now.day}日{now.hour}时"
        result["params"] = {
            "year": year_num, "month": month_num, "day": day_num, "hour": hour_num
        }
        
        # 上卦 = 年+月+日
        upper_num = (year_num + month_num + day_num) % 8
        upper_gua = num_to_gua(upper_num)
        
        # 下卦 = 年+月+日+时
        lower_num = (year_num + month_num + day_num + hour_num) % 8
        lower_gua = num_to_gua(lower_num)
        
        # 动爻 = 年+月+日+时
        dongyao = (year_num + month_num + day_num + hour_num) % 6
    
    # 本卦
    ben_gua = f"{upper_gua}{lower_gua}"
    result["ben_gua"] = {
        "name": ben_gua,
        "symbol": f"{BAGUA_SYMBOL[upper_gua]}{BAGUA_SYMBOL[lower_gua]}",
        "upper": upper_gua,
        "lower": lower_gua
    }
    
    # 互卦
    hu_upper = HU_GUA_MAP[upper_gua]["上"]
    hu_lower = HU_GUA_MAP[lower_gua]["下"]
    hu_gua = f"{hu_upper}{hu_lower}"
    result["hu_gua"] = {
        "name": hu_gua,
        "symbol": f"{BAGUA_SYMBOL[hu_upper]}{BAGUA_SYMBOL[hu_lower]}",
        "upper": hu_upper,
        "lower": hu_lower
    }
    
    # 之卦
    # 动爻在下卦则变下卦，在上卦则变上卦
    if dongyao < 3:
        # 下卦动爻，变下卦
        lower_binary = ["1" if BAGUA_NUM[lower_gua] & (1 << (2-dongyao)) else "0" for dongyao in range(3)]
        lower_binary[dongyao] = "1" if lower_binary[dongyao] == "0" else "0"
        new_lower_num = sum([int(lower_binary[i]) * (1 << (2-i)) for i in range(3)])
        new_lower_gua = num_to_gua(new_lower_num)
        zhi_gua = f"{upper_gua}{new_lower_gua}"
    else:
        # 上卦动爻，变上卦
        upper_binary = ["1" if BAGUA_NUM[upper_gua] & (1 << (5-dongyao)) else "0" for dongyao in range(3, 6)]
        upper_binary[dongyao-3] = "1" if upper_binary[dongyao-3] == "0" else "0"
        new_upper_num = sum([int(upper_binary[i-3]) * (1 << (5-i)) for i in range(3, 6)])
        new_upper_gua = num_to_gua(new_upper_num)
        zhi_gua = f"{new_upper_gua}{lower_gua}"
    
    result["zhi_gua"] = {
        "name": zhi_gua,
        "symbol": f"{BAGUA_SYMBOL[zhi_gua[0]]}{BAGUA_SYMBOL[zhi_gua[1]]}",
        "dongyao": dongyao
    }
    
    # 体用分析
    # 动爻在下卦则上卦为体，下卦为用
    # 动爻在上卦则下卦为体，上卦为用
    if dongyao < 3:
        ti_gua = upper_gua
        yong_gua = lower_gua
    else:
        ti_gua = lower_gua
        yong_gua = upper_gua
    
    ti_wuxing = BAGUA_WUXING[ti_gua]
    yong_wuxing = BAGUA_WUXING[yong_gua]
    shengke_type, shengke_desc = wuxing_sheng_ke(yong_wuxing, ti_wuxing)
    
    result["ti_yong"] = {
        "ti": ti_gua,
        "yong": yong_gua,
        "ti_wuxing": ti_wuxing,
        "yong_wuxing": yong_wuxing,
        "relationship": shengke_type,
        "description": shengke_desc
    }
    
    # 吉凶判断
    if shengke_type == "被生":
        result["judgment"] = "大吉"
        result["judgment_desc"] = f"用生体，得生扶，大吉"
    elif shengke_type == "生":
        result["judgment"] = "平"
        result["judgment_desc"] = f"用克体，需泄气，平"
    elif shengke_type == "被克":
        result["judgment"] = "凶"
        result["judgment_desc"] = f"用克体，受克制，凶"
    else:
        result["judgment"] = "中平"
        result["judgment_desc"] = f"体用五行相同，中平"
    
    result["dongyao_position"] = ["初", "二", "三", "四", "五", "上"][dongyao] if dongyao < 6 else "无"
    
    return result

def main():
    parser = argparse.ArgumentParser(description="梅花易数计算")
    parser.add_argument("--year", type=int, help="年份（时间卦）")
    parser.add_argument("--month", type=int, help="月份（时间卦）")
    parser.add_argument("--day", type=int, help="日期（时间卦）")
    parser.add_argument("--hour", type=int, help="时辰（时间卦）")
    parser.add_argument("--num1", type=int, help="第一个数字（数字卦）")
    parser.add_argument("--num2", type=int, help="第二个数字（数字卦）")
    parser.add_argument("--num3", type=int, help="第三个数字（数字卦）")
    parser.add_argument("--num4", type=int, help="第四个数字（数字卦）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 计算梅花易数
    result = calculate_plum_blossom(
        args.year, args.month, args.day, args.hour,
        args.num1, args.num2, args.num3, args.num4
    )
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print(f"【梅花易数】{result['method']}")
        print("=" * 60)
        print(f"\n输入参数：{result.get('input', '')}")
        
        print(f"\n【本卦】{result['ben_gua']['name']} {result['ben_gua']['symbol']}")
        print(f"  上卦：{result['ben_gua']['upper']}（{BAGUA_WUXING[result['ben_gua']['upper']]}）")
        print(f"  下卦：{result['ben_gua']['lower']}（{BAGUA_WUXING[result['ben_gua']['lower']]}）")
        
        print(f"\n【互卦】{result['hu_gua']['name']} {result['hu_gua']['symbol']}")
        print(f"  上互：{result['hu_gua']['upper']}")
        print(f"  下互：{result['hu_gua']['lower']}")
        
        print(f"\n【之卦】{result['zhi_gua']['name']} {result['zhi_gua']['symbol']}")
        print(f"  动爻：{result['dongyao_position']}爻")
        
        print(f"\n【体用分析】")
        print(f"  体卦：{result['ti_yong']['ti']}（{result['ti_yong']['ti_wuxing']}）")
        print(f"  用卦：{result['ti_yong']['yong']}（{result['ti_yong']['yong_wuxing']}）")
        print(f"  关系：{result['ti_yong']['description']}")
        
        print(f"\n【吉凶判断】")
        print(f"  {result['judgment']} - {result['judgment_desc']}")
        
        print("=" * 60)

if __name__ == "__main__":
    main()
