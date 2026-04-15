#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
旺相休囚死计算脚本
根据五行和时间，计算五行在当前时间的旺相休囚死状态
"""

import argparse
import json
from datetime import datetime


# 五行对应的季节
WUXING_SEASON = {
    '木': '春',
    '火': '夏',
    '土': '长夏',
    '金': '秋',
    '水': '冬',
}

# 季节对应的月份（农历）
SEASON_MONTH = {
    '春': [1, 2, 3],    # 寅月、卯月、辰月
    '夏': [4, 5, 6],    # 巳月、未月、午月
    '长夏': [6],        # 未月（长夏）
    '秋': [7, 8, 9],    # 申月、酉月、戌月
    '冬': [10, 11, 12], # 亥月、子月、丑月
}

# 旺相休囚死规则
# 旺：当令得时
# 相：得相生
# 休：失令（被旺者所生）
# 囚：被克
# 死：被旺者所克（最衰）
WUXING_NAMES = ['金', '木', '水', '火', '土']

WANG_XIANG_RULES = {
    # 木旺于春
    '春': {
        '木': '旺',
        '火': '相',  # 木生火
        '土': '死',  # 木克土
        '金': '囚',  # 金克木，但木旺
        '水': '休',  # 水生木
    },
    # 火旺于夏
    '夏': {
        '火': '旺',
        '土': '相',  # 火生土
        '金': '死',  # 火克金
        '水': '囚',  # 水克火，但火旺
        '木': '休',  # 木生火
    },
    # 土旺于长夏
    '长夏': {
        '土': '旺',
        '金': '相',  # 土生金
        '水': '死',  # 土克水
        '木': '囚',  # 木克土，但土旺
        '火': '休',  # 火生土
    },
    # 金旺于秋
    '秋': {
        '金': '旺',
        '水': '相',  # 金生水
        '木': '死',  # 金克木
        '火': '囚',  # 火克金，但金旺
        '土': '休',  # 土生金
    },
    # 水旺于冬
    '冬': {
        '水': '旺',
        '木': '相',  # 水生木
        '火': '死',  # 水克火
        '土': '囚',  # 土克水，但水旺
        '金': '休',  # 金生水
    },
}

# 月份名称（农历）
MONTH_NAMES = {
    1: '寅月', 2: '卯月', 3: '辰月',
    4: '巳月', 5: '午月', 6: '未月',
    7: '申月', 8: '酉月', 9: '戌月',
    10: '亥月', 11: '子月', 12: '丑月',
}


def get_season_from_month(month):
    """
    根据月份获取季节

    参数:
    month: 月份（1-12，农历）

    返回:
    季节名称
    """
    for season, months in SEASON_MONTH.items():
        if month in months:
            return season
    return None


def calculate_wangxiang(wuxing, month):
    """
    计算五行在指定月份的旺相休囚死

    参数:
    wuxing: 五行（金、木、水、火、土）
    month: 月份（1-12，农历）

    返回:
    旺相休囚死状态
    """
    if wuxing not in WUXING_NAMES:
        raise ValueError(f"未知五行: {wuxing}")

    if month < 1 or month > 12:
        raise ValueError(f"月份必须在1-12之间: {month}")

    # 获取季节
    season = get_season_from_month(month)
    if not season:
        raise ValueError(f"无法确定季节: {month}月")

    # 获取旺相休囚死规则
    rules = WANG_XIANG_RULES.get(season, {})
    state = rules.get(wuxing, '未知')

    # 状态描述
    state_meaning = {
        '旺': '最强盛，得令当权',
        '相': '次强盛，得相生扶',
        '休': '休息状态，失令',
        '囚': '受制约，被克',
        '死': '最衰弱，被旺者所克',
    }

    return {
        'wuxing': wuxing,
        'month': month,
        'month_name': MONTH_NAMES.get(month, f'{month}月'),
        'season': season,
        'state': state,
        'meaning': state_meaning.get(state, '未知'),
    }


def get_current_lunar_month():
    """
    获取当前农历月份（简化版，实际应使用农历库）

    注意：这是一个简化版本，实际应用中应该使用专业的农历转换库
    如: lunar, zhdate 等
    """
    # 简化处理：假设当前是公历，粗略对应农历
    now = datetime.now()
    # 简化算法：公历月份对应农历（不精确）
    lunar_month = now.month % 12
    if lunar_month == 0:
        lunar_month = 12
    return lunar_month


def main():
    parser = argparse.ArgumentParser(description='旺相休囚死计算工具')
    parser.add_argument('--wuxing', required=True, help='五行（金、木、水、火、土）')
    parser.add_argument('--month', type=int, help='月份（1-12，农历），不指定则使用当前时间')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    try:
        # 获取月份
        if args.month:
            month = args.month
        else:
            month = get_current_lunar_month()

        # 计算旺相休囚死
        result = calculate_wangxiang(args.wuxing, month)
        result['status'] = 'success'

        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 文本格式输出
            print(f"旺相休囚死分析:")
            print(f"  五行: {result['wuxing']}")
            print(f"  时间: {result['month_name']}（{result['season']}）")
            print(f"  状态: {result['state']} - {result['meaning']}")

    except ValueError as e:
        result = {
            'status': 'error',
            'message': str(e)
        }
        print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
