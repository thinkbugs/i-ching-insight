#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
婚恋匹配度计算脚本
根据双方的八卦性格，计算婚恋匹配度
"""

import argparse
import json


# 八卦性格特征
BAGUA_PERSONALITY = {
    '乾': {
        'gender': '男',
        'traits': ['刚强', '主动', '领导力强', '果断', '有野心'],
        'description': '刚强果断，具有领导力和野心，适合主导',
        'best_match': ['坤', '兑'],
        'avoid_match': ['巽', '艮'],
    },
    '坤': {
        'gender': '女',
        'traits': ['柔顺', '包容', '温和', '细心', '顾家'],
        'description': '柔顺包容，温和细心，适合配合',
        'best_match': ['乾', '震'],
        'avoid_match': ['巽', '离'],
    },
    '震': {
        'gender': '男',
        'traits': ['震动', '启动', '进取', '有活力', '冲动'],
        'description': '震动启动，有活力和进取心，但容易冲动',
        'best_match': ['坤', '巽'],
        'avoid_match': ['艮', '兑'],
    },
    '巽': {
        'gender': '女',
        'traits': ['顺从', '渗透', '灵活', '细腻', '敏感'],
        'description': '顺从渗透，灵活细腻，但容易敏感',
        'best_match': ['震', '坎'],
        'avoid_match': ['乾', '艮'],
    },
    '坎': {
        'gender': '男',
        'traits': ['陷险', '深沉', '内敛', '神秘', '坚韧'],
        'description': '陷险深沉，内敛神秘，但坚韧不拔',
        'best_match': ['离', '巽'],
        'avoid_match': ['震', '艮'],
    },
    '离': {
        'gender': '女',
        'traits': ['光明', '热情', '外向', '积极', '情绪化'],
        'description': '光明热情，外向积极，但容易情绪化',
        'best_match': ['坎', '震'],
        'avoid_match': ['坤', '艮'],
    },
    '艮': {
        'gender': '男',
        'traits': ['静止', '稳定', '固执', '保守', '踏实'],
        'description': '静止稳定，固执保守，但踏实可靠',
        'best_match': ['兑', '离'],
        'avoid_match': ['震', '巽'],
    },
    '兑': {
        'gender': '女',
        'traits': ['喜悦', '沟通', '温柔', '善解人意', '情绪波动'],
        'description': '喜悦沟通，温柔善解人意，但情绪波动',
        'best_match': ['乾', '艮'],
        'avoid_match': ['坎', '离'],
    },
}


def calculate_match_score(trigram1, trigram2):
    """
    计算两个八卦的匹配度

    参数:
    trigram1: 第一个八卦
    trigram2: 第二个八卦

    返回:
    匹配度分数和说明
    """
    if trigram1 not in BAGUA_PERSONALITY or trigram2 not in BAGUA_PERSONALITY:
        raise ValueError(f"未知八卦: {trigram1}或{trigram2}")

    info1 = BAGUA_PERSONALITY[trigram1]
    info2 = BAGUA_PERSONALITY[trigram2]

    # 基础分数
    base_score = 50

    # 阴阳配合分数（阴阳相配加分）
    # 乾、震、坎、艮为阳卦
    # 坤、巽、离、兑为阴卦
    yang_trigrams = ['乾', '震', '坎', '艮']
    yin_trigrams = ['坤', '巽', '离', '兑']

    if (trigram1 in yang_trigrams and trigram2 in yin_trigrams) or \
       (trigram1 in yin_trigrams and trigram2 in yang_trigrams):
        base_score += 20  # 阴阳相配

    # 最佳匹配加分
    if trigram2 in info1['best_match']:
        base_score += 30
    elif trigram1 in info2['best_match']:
        base_score += 30

    # 避免匹配减分
    if trigram2 in info1['avoid_match']:
        base_score -= 20
    elif trigram1 in info2['avoid_match']:
        base_score -= 20

    # 限制分数在0-100之间
    score = max(0, min(100, base_score))

    # 生成匹配度说明
    if score >= 80:
        match_level = '极佳'
        description = '天生一对，性格互补，非常适合在一起'
    elif score >= 60:
        match_level = '良好'
        description = '性格相配，可以在一起，但需要磨合'
    elif score >= 40:
        match_level = '一般'
        description = '性格一般，需要努力经营才能维持关系'
    else:
        match_level = '较差'
        description = '性格不合，建议慎重考虑'

    return {
        'score': score,
        'level': match_level,
        'description': description,
    }


def marriage_match_analysis(trigram1, trigram2):
    """
    婚恋匹配分析

    参数:
    trigram1: 一方的八卦性格
    trigram2: 另一方的八卦性格

    返回:
    匹配分析结果
    """
    if trigram1 not in BAGUA_PERSONALITY or trigram2 not in BAGUA_PERSONALITY:
        raise ValueError(f"未知八卦: {trigram1}或{trigram2}")

    info1 = BAGUA_PERSONALITY[trigram1]
    info2 = BAGUA_PERSONALITY[trigram2]

    # 计算匹配度
    match_result = calculate_match_score(trigram1, trigram2)

    # 生成建议
    suggestions = []

    # 阴阳平衡建议
    yang_trigrams = ['乾', '震', '坎', '艮']
    yin_trigrams = ['坤', '巽', '离', '兑']

    if trigram1 in yang_trigrams and trigram2 in yang_trigrams:
        suggestions.append('双方都偏阳刚，建议一方多些柔顺')
    elif trigram1 in yin_trigrams and trigram2 in yin_trigrams:
        suggestions.append('双方都偏阴柔，建议一方多些主动')

    # 性格互补建议
    if '刚强' in info1['traits'] and '柔顺' in info2['traits']:
        suggestions.append('性格互补，刚柔并济')
    elif '柔顺' in info1['traits'] and '刚强' in info2['traits']:
        suggestions.append('性格互补，刚柔并济')

    # 沟通建议
    if '沟通' not in info1['traits'] and '沟通' not in info2['traits']:
        suggestions.append('建议加强沟通，多交流')

    # 情绪管理建议
    if '情绪化' in info1['traits'] or '情绪化' in info2['traits']:
        suggestions.append('注意情绪管理，避免冲动')

    return {
        'status': 'success',
        'person1': {
            'trigram': trigram1,
            'description': info1['description'],
            'traits': info1['traits'],
        },
        'person2': {
            'trigram': trigram2,
            'description': info2['description'],
            'traits': info2['traits'],
        },
        'match_result': match_result,
        'suggestions': suggestions,
    }


def main():
    parser = argparse.ArgumentParser(description='婚恋匹配度计算工具')
    parser.add_argument('--trigram1', required=True, help='一方的八卦性格（乾、坤、震、巽、坎、离、艮、兑）')
    parser.add_argument('--trigram2', required=True, help='另一方的八卦性格（乾、坤、震、巽、坎、离、艮、兑）')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    try:
        # 婚恋匹配分析
        result = marriage_match_analysis(args.trigram1, args.trigram2)

        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 文本格式输出
            print(f"婚恋匹配分析")
            print()
            print(f"男方: {result['person1']['trigram']}卦")
            print(f"  描述: {result['person1']['description']}")
            print(f"  特质: {', '.join(result['person1']['traits'])}")
            print()
            print(f"女方: {result['person2']['trigram']}卦")
            print(f"  描述: {result['person2']['description']}")
            print(f"  特质: {', '.join(result['person2']['traits'])}")
            print()
            print(f"匹配度: {result['match_result']['score']}分 - {result['match_result']['level']}")
            print(f"说明: {result['match_result']['description']}")
            print()
            if result['suggestions']:
                print("建议:")
                for suggestion in result['suggestions']:
                    print(f"  • {suggestion}")

    except ValueError as e:
        result = {
            'status': 'error',
            'message': str(e)
        }
        print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
