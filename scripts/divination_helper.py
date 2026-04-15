#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
起卦工具脚本
功能：支持金钱卦、时间卦、数字卦、揲蓍法四种起卦方法
"""

import argparse
import json
import random
import datetime
from typing import List, Tuple

# 阴阳爻
YIN = 0
YANG = 1

# 卦象符号
YIN_SYMBOL = "— —"
YANG_SYMBOL = "————"

def divination_by_coin(num_coins: int = 3) -> Tuple[List[int], List[int]]:
    """
    金钱卦（三枚硬币法）
    
    原理：
    - 每次抛掷3枚硬币
    - 背面（字）=2，正面（花）=3
    - 总和：6（老阴），7（少阳），8（少阴），9（老阳）
    - 从下往上抛6次得到六爻
    
    Returns:
        (六爻列表, 动爻列表)
    """
    yao_list = []
    moving_positions = []
    
    print("\n【金钱卦起卦】")
    print("请抛掷3枚硬币，每次记录正面（花）数量：")
    print("  - 0个正面（3背）= 少阳（阳爻不动）")
    print("  - 1个正面（2背1花）= 少阴（阴爻不动）")
    print("  - 2个正面（1背2花）= 少阳（阳爻不动）")
    print("  - 3个正面（0背3花）= 老阴（阴爻动）")
    print("  - 注：传统金钱卦使用2/3计算，这里简化为抛硬币模拟\n")
    
    for i in range(6):
        # 模拟抛掷3枚硬币（0=背/字=2，1=正/花=3）
        coins = [random.randint(0, 1) for _ in range(3)]
        heads = sum(coins)  # 正面数量
        
        # 计算总和（背面=2，正面=3）
        total = sum(2 if c == 0 else 3 for c in coins)
        
        # 判断爻的性质
        if total == 6:  # 老阴
            yao = YIN
            moving_positions.append(i)
            yao_type = "老阴（动）"
        elif total == 7:  # 少阳
            yao = YANG
            yao_type = "少阳（不动）"
        elif total == 8:  # 少阴
            yao = YIN
            yao_type = "少阴（不动）"
        else:  # total == 9, 老阳
            yao = YANG
            moving_positions.append(i)
            yao_type = "老阳（动）"
        
        yao_list.append(yao)
        
        position_name = ["初", "二", "三", "四", "五", "上"][i]
        symbol = YANG_SYMBOL if yao == YANG else YIN_SYMBOL
        print(f"第{i+1}掷（{position_name}爻）: 正面{heads}枚 → {total} → {yao_type} {symbol}")
    
    return yao_list, moving_positions

def divination_by_time(year: int = None, month: int = None, day: int = None, hour: int = None) -> Tuple[List[int], List[int]]:
    """
    时间卦（按年月日时起卦）
    
    原理：
    - 上卦 = (年+月+日) % 8
    - 下卦 = (年+月+日+时) % 8
    - 动爻 = (年+月+日+时) % 6
    
    Returns:
        (六爻列表, 动爻列表)
    """
    if year is None:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
    
    # 天干地支纪年转换（简化版，使用公历年份）
    # 1984年为甲子年，每60年一循环
    base_year = 1984
    cycle = (year - base_year) % 60
    gan_zhi_year = cycle
    
    # 月份修正（农历月份1-12）
    lunar_month = month
    
    # 时辰修正（子时=23-1点，丑时=1-3点...）
    shichen = (hour + 1) // 2 % 12
    
    # 计算上下卦
    upper_gua_num = (gan_zhi_year + lunar_month + day) % 8
    lower_gua_num = (gan_zhi_year + lunar_month + day + shichen) % 8
    dongyao_num = (gan_zhi_year + lunar_month + day + shichen) % 6
    
    # 八卦对应的二进制（从下往上）
    # 乾=111, 兑=011, 离=101, 震=001, 巽=110, 坎=010, 艮=100, 坤=000
    gua_to_binary = {
        1: [1, 1, 1],   # 乾
        2: [0, 1, 1],   # 兑
        3: [1, 0, 1],   # 离
        4: [0, 0, 1],   # 震
        5: [1, 1, 0],   # 巽
        6: [0, 1, 0],   # 坎
        7: [1, 0, 0],   # 艮
        0: [0, 0, 0]    # 坤
    }
    
    # 组合六爻（上卦+下卦）
    upper_binary = gua_to_binary[upper_gua_num]
    lower_binary = gua_to_binary[lower_gua_num]
    yao_list = lower_binary + upper_binary
    
    # 动爻位置（从下往上，0-5）
    moving_positions = [dongyao_num] if dongyao_num != 0 else []
    
    # 八卦名称
    gua_names = ["坤", "乾", "兑", "离", "震", "巽", "坎", "艮"]
    
    print(f"\n【时间卦起卦】")
    print(f"起卦时间：{year}年{month}月{day}日{hour}时")
    print(f"年月日时：{gan_zhi_year}+{lunar_month}+{day}+{shichen}")
    print(f"上卦：({gan_zhi_year}+{lunar_month}+{day})%8 = {upper_gua_num}（{gua_names[upper_gua_num]}）")
    print(f"下卦：({gan_zhi_year}+{lunar_month}+{day}+{shichen})%8 = {lower_gua_num}（{gua_names[lower_gua_num]}）")
    print(f"动爻：({gan_zhi_year}+{lunar_month}+{day}+{shichen})%6 = {dongyao_num}")
    if dongyao_num != 0:
        print(f"动爻位置：{'初二三四五上'[dongyao_num]}爻")
    else:
        print("动爻位置：无")
    
    return yao_list, moving_positions

def divination_by_number(num1: int = None, num2: int = None, num3: int = None) -> Tuple[List[int], List[int]]:
    """
    数字卦（三个数起卦）
    
    原理：
    - 上卦 = 第1个数 % 8
    - 下卦 = 第2个数 % 8
    - 动爻 = 第3个数 % 6
    
    Returns:
        (六爻列表, 动爻列表)
    """
    if num1 is None:
        num1 = random.randint(1, 999)
    if num2 is None:
        num2 = random.randint(1, 999)
    if num3 is None:
        num3 = random.randint(1, 999)
    
    upper_gua_num = num1 % 8
    lower_gua_num = num2 % 8
    dongyao_num = num3 % 6
    
    # 八卦对应的二进制
    gua_to_binary = {
        1: [1, 1, 1],   # 乾
        2: [0, 1, 1],   # 兑
        3: [1, 0, 1],   # 离
        4: [0, 0, 1],   # 震
        5: [1, 1, 0],   # 巽
        6: [0, 1, 0],   # 坎
        7: [1, 0, 0],   # 艮
        0: [0, 0, 0]    # 坤
    }
    
    upper_binary = gua_to_binary[upper_gua_num]
    lower_binary = gua_to_binary[lower_gua_num]
    yao_list = lower_binary + upper_binary
    
    moving_positions = [dongyao_num] if dongyao_num != 0 else []
    
    gua_names = ["坤", "乾", "兑", "离", "震", "巽", "坎", "艮"]
    
    print(f"\n【数字卦起卦】")
    print(f"三个数字：{num1}, {num2}, {num3}")
    print(f"上卦：{num1}%8 = {upper_gua_num}（{gua_names[upper_gua_num]}）")
    print(f"下卦：{num2}%8 = {lower_gua_num}（{gua_names[lower_gua_num]}）")
    print(f"动爻：{num3}%6 = {dongyao_num}")
    if dongyao_num != 0:
        print(f"动爻位置：{'初二三四五上'[dongyao_num]}爻")
    else:
        print("动爻位置：无")
    
    return yao_list, moving_positions

def divination_by_stick() -> Tuple[List[int], List[int]]:
    """
    揲蓍法（大衍之数）
    
    原理：
    - 使用50根蓍草，先取1根不用
    - 剩余49根，分二、挂一、揲四、归奇
    - 重复3次，得到每爻的数字（6/7/8/9）
    - 从下往上做6次，得到六爻
    
    Returns:
        (六爻列表, 动爻列表)
    """
    print("\n【揲蓍法起卦】（模拟）")
    print("使用50根蓍草，取1根不用，剩余49根\n")
    
    yao_list = []
    moving_positions = []
    
    for i in range(6):
        # 模拟揲蓍过程（简化版）
        # 实际揲謴需要手工操作，这里用随机数模拟结果
        
        # 生成一个6/7/8/9的随机数
        total = random.choice([6, 7, 8, 9])
        
        # 判断爻的性质
        if total == 6:  # 老阴
            yao = YIN
            moving_positions.append(i)
            yao_type = "老阴（动）"
        elif total == 7:  # 少阳
            yao = YANG
            yao_type = "少阳（不动）"
        elif total == 8:  # 少阴
            yao = YIN
            yao_type = "少阴（不动）"
        else:  # total == 9, 老阳
            yao = YANG
            moving_positions.append(i)
            yao_type = "老阳（动）"
        
        yao_list.append(yao)
        
        position_name = ["初", "二", "三", "四", "五", "上"][i]
        symbol = YANG_SYMBOL if yao == YANG else YIN_SYMBOL
        print(f"第{i+1}变（{position_name}爻）: {total} → {yao_type} {symbol}")
    
    print(f"\n揲謴说明：")
    print(f"• 6 = 老阴（阴爻动变阳）")
    print(f"• 7 = 少阳（阳爻不动）")
    print(f"• 8 = 少阴（阴爻不动）")
    print(f"• 9 = 老阳（阳爻动变阴）")
    
    return yao_list, moving_positions

def display_hexagram(yao_list: List[int], moving_positions: List[int]):
    """
    显示卦象
    """
    print("\n【所得卦象】")
    print("━━━━━━━━━━━━━━")
    
    position_names = ["上", "五", "四", "三", "二", "初"]
    
    for i in range(5, -1, -1):  # 从上到下显示
        yao = yao_list[i]
        symbol = YANG_SYMBOL if yao == YANG else YIN_SYMBOL
        
        # 标记动爻
        if i in moving_positions:
            marker = " ○" if yao == YANG else " ×"
        else:
            marker = ""
        
        print(f"{position_names[i]}爻：{symbol}{marker}")
    
    print("━━━━━━━━━━━━━━")
    print(f"动爻位置：{', '.join(['初二三四五上'[i] + '爻' for i in moving_positions]) if moving_positions else '无'}")
    print(f"二进制：{''.join(map(str, yao_list))}")

def main():
    parser = argparse.ArgumentParser(description="起卦工具")
    parser.add_argument("--method", required=True, choices=["coin", "time", "number", "stick"],
                        help="起卦方法：coin=金钱卦，time=时间卦，number=数字卦，stick=揲蓍法")
    parser.add_argument("--year", type=int, help="年份（时间卦）")
    parser.add_argument("--month", type=int, help="月份（时间卦）")
    parser.add_argument("--day", type=int, help="日期（时间卦）")
    parser.add_argument("--hour", type=int, help="时辰（时间卦）")
    parser.add_argument("--num1", type=int, help="第一个数字（数字卦）")
    parser.add_argument("--num2", type=int, help="第二个数字（数字卦）")
    parser.add_argument("--num3", type=int, help="第三个数字（数字卦）")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 根据方法起卦
    if args.method == "coin":
        yao_list, moving_positions = divination_by_coin()
    elif args.method == "time":
        yao_list, moving_positions = divination_by_time(args.year, args.month, args.day, args.hour)
    elif args.method == "number":
        yao_list, moving_positions = divination_by_number(args.num1, args.num2, args.num3)
    elif args.method == "stick":
        yao_list, moving_positions = divination_by_stick()
    else:
        print(json.dumps({"error": "未知的起卦方法"}, ensure_ascii=False))
        return
    
    # 显示卦象（文本模式）
    if args.format == "text":
        display_hexagram(yao_list, moving_positions)
    
    # 输出结果
    result = {
        "method": args.method,
        "method_name": {
            "coin": "金钱卦",
            "time": "时间卦",
            "number": "数字卦",
            "stick": "揲蓍法"
        }[args.method],
        "yao_list": yao_list,
        "moving_positions": moving_positions,
        "moving_count": len(moving_positions),
        "binary": "".join(map(str, yao_list)),
        "hexagram_symbol": "".join([YANG_SYMBOL if y == YANG else YIN_SYMBOL for y in yao_list]),
        "next_steps": [
            "使用 python scripts/hexagram_calculator.py 解析本卦",
            "使用 python scripts/dongyao_simulator.py 推演爻变",
            "使用 python scripts/yao_position_analyzer.py 分析爻位"
        ]
    }
    
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
