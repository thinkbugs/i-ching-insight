#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
五行分析脚本
判断两个五行之间的生克关系
"""

import argparse
import json


# 五行生克关系
WUXING_SHENG = {
    '木': '火',  # 木生火
    '火': '土',  # 火生土
    '土': '金',  # 土生金
    '金': '水',  # 金生水
    '水': '木',  # 水生木
}

WUXING_KE = {
    '木': '土',  # 木克土
    '土': '水',  # 土克水
    '水': '火',  # 水克火
    '火': '金',  # 火克金
    '金': '木',  # 金克木
}

WUXING_NAMES = ['金', '木', '水', '火', '土']


def analyze_wuxing_relation(wuxing1, wuxing2):
    """
    分析两个五行之间的关系

    参数:
    wuxing1: 第一个五行（金、木、水、火、土）
    wuxing2: 第二个五行（金、木、水、火、土）

    返回:
    关系类型（生、克、被生、被克、同类）
    """
    if wuxing1 not in WUXING_NAMES or wuxing2 not in WUXING_NAMES:
        raise ValueError(f"五行必须是: {', '.join(WUXING_NAMES)}")

    # 同类
    if wuxing1 == wuxing2:
        return {
            'relation': '同类',
            'meaning': f'{wuxing1}与{wuxing2}为同类',
            'strength': 0,  # 强度中性
        }

    # 生：wuxing1生wuxing2
    if WUXING_SHENG.get(wuxing1) == wuxing2:
        return {
            'relation': '生',
            'meaning': f'{wuxing1}生{wuxing2}',
            'direction': f'{wuxing1} -> {wuxing2}',
            'strength': 1,  # 正向影响
        }

    # 克：wuxing1克wuxing2
    if WUXING_KE.get(wuxing1) == wuxing2:
        return {
            'relation': '克',
            'meaning': f'{wuxing1}克{wuxing2}',
            'direction': f'{wuxing1} -> {wuxing2}',
            'strength': -1,  # 负向影响
        }

    # 被生：wuxing2生wuxing1
    if WUXING_SHENG.get(wuxing2) == wuxing1:
        return {
            'relation': '被生',
            'meaning': f'{wuxing2}生{wuxing1}（{wuxing1}被{wuxing2}生）',
            'direction': f'{wuxing2} -> {wuxing1}',
            'strength': 2,  # 被生是正面影响
        }

    # 被克：wuxing2克wuxing1
    if WUXING_KE.get(wuxing2) == wuxing1:
        return {
            'relation': '被克',
            'meaning': f'{wuxing2}克{wuxing1}（{wuxing1}被{wuxing2}克）',
            'direction': f'{wuxing2} -> {wuxing1}',
            'strength': -2,  # 被克是负面影响
        }

    # 理论上不应该到这里
    return {
        'relation': '未知',
        'meaning': f'{wuxing1}与{wuxing2}关系不明',
    }


def calculate_wuxing_balance(wuxing_list):
    """
    计算五行平衡

    参数:
    wuxing_list: 五行列表，如 ['木', '火', '土', '金', '水']

    返回:
    五行分布和平衡分析
    """
    if not wuxing_list:
        return {
            'status': 'error',
            'message': '五行列表不能为空'
        }

    # 统计五行数量
    count = {w: 0 for w in WUXING_NAMES}
    for w in wuxing_list:
        if w in count:
            count[w] += 1
        else:
            return {
                'status': 'error',
                'message': f'未知五行: {w}'
            }

    total = len(wuxing_list)

    # 判断平衡
    max_count = max(count.values())
    min_count = min(count.values())
    balance_ratio = max_count / total if total > 0 else 0

    if balance_ratio > 0.5:
        balance_status = '失衡'
        balance_meaning = f'五行严重失衡，{max(count, key=count.get)}过旺'
    elif balance_ratio > 0.33:
        balance_status = '偏颇'
        balance_meaning = f'五行偏向，{max(count, key=count.get)}较旺'
    else:
        balance_status = '平衡'
        balance_meaning = '五行相对平衡'

    return {
        'status': 'success',
        'total': total,
        'distribution': count,
        'balance_status': balance_status,
        'balance_meaning': balance_meaning,
        'dominant': max(count, key=count.get) if count else None,
    }


def main():
    parser = argparse.ArgumentParser(description='五行分析工具')
    parser.add_argument('--wuxing1', help='第一个五行（金、木、水、火、土）')
    parser.add_argument('--wuxing2', help='第二个五行（金、木、水、火、土）')
    parser.add_argument('--balance', help='五行平衡分析，用逗号分隔。例如: 木,火,土,金,水')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    result = {}

    # 五行关系分析
    if args.wuxing1 and args.wuxing2:
        try:
            relation = analyze_wuxing_relation(args.wuxing1, args.wuxing2)
            result['relation'] = relation
        except ValueError as e:
            result['error'] = str(e)

    # 五行平衡分析
    if args.balance:
        wuxing_list = [w.strip() for w in args.balance.split(',')]
        balance = calculate_wuxing_balance(wuxing_list)
        result['balance'] = balance

    if not result:
        result = {
            'status': 'error',
            'message': '请提供--wuxing1和--wuxing2进行关系分析，或提供--balance进行平衡分析'
        }

    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        if 'relation' in result:
            r = result['relation']
            print(f"五行关系分析:")
            print(f"  {args.wuxing1} 与 {args.wuxing2}: {r['meaning']}")
            if 'direction' in r:
                print(f"  方向: {r['direction']}")

        if 'balance' in result:
            b = result['balance']
            if b['status'] == 'success':
                print(f"\n五行平衡分析:")
                print(f"  总数: {b['total']}")
                print(f"  分布: {b['distribution']}")
                print(f"  状态: {b['balance_status']} - {b['balance_meaning']}")
                print(f"  主导五行: {b['dominant']}")
            else:
                print(f"错误: {b['message']}")

        if 'error' in result:
            print(f"错误: {result['error']}")


if __name__ == '__main__':
    main()
