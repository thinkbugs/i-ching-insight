#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纳甲纳支脚本
为八卦的每一爻配置天干地支
"""

import argparse
import json


# 八卦纳甲表
NAYI_TABLE = {
    '乾': {'nagan': ['甲', '壬'], 'nazhi': ['子', '寅', '辰', '午', '申', '戌']},
    '坤': {'nagan': ['乙', '癸'], 'nazhi': ['未', '巳', '卯', '丑', '亥', '酉']},
    '震': {'nagan': ['庚'], 'nazhi': ['子', '寅', '辰', '午', '申', '戌']},
    '巽': {'nagan': ['辛'], 'nazhi': ['丑', '亥', '酉', '未', '巳', '卯']},
    '坎': {'nagan': ['戊'], 'nazhi': ['寅', '辰', '午', '申', '戌', '子']},
    '离': {'nagan': ['己'], 'nazhi': ['巳', '未', '酉', '亥', '丑', '卯']},
    '艮': {'nagan': ['丙'], 'nazhi': ['辰', '午', '申', '戌', '子', '寅']},
    '兑': {'nagan': ['丁'], 'nazhi': ['巳', '未', '酉', '亥', '丑', '卯']},
}

# 地支五行
DIZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水',
}

# 天干五行
TIANGAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土',
    '庚': '金', '辛': '金', '壬': '水', '癸': '水',
}

# 爻位名称
YAO_NAMES = ['初', '二', '三', '四', '五', '上']


def calculate_nayi(trigram_name):
    """
    计算八卦的纳甲纳支
    trigram_name: 八卦名称（乾、坤、震、巽、坎、离、艮、兑）
    """
    if trigram_name not in NAYI_TABLE:
        raise ValueError(f"未知八卦: {trigram_name}")

    nayi_info = NAYI_TABLE[trigram_name]

    # 配置天干
    if len(nayi_info['nagan']) == 1:
        # 只有一个天干，六爻都配这个天干
        nagan = nayi_info['nagan'] * 6
    else:
        # 两个天干，前三爻配第一个，后三爻配第二个
        nagan = [nayi_info['nagan'][0]] * 3 + [nayi_info['nagan'][1]] * 3

    # 配置地支
    nazhi = nayi_info['nazhi']

    # 构建结果
    result = []
    for i in range(6):
        yao_name = YAO_NAMES[i]
        nagan_gan = nagan[i]
        nazhi_zhi = nazhi[i]

        # 五行
        wuxing = DIZHI_WUXING[nazhi_zhi]

        result.append({
            'position': i + 1,  # 爻位（1-6）
            'name': yao_name,
            'tiangan': nagan_gan,
            'dizhi': nazhi_zhi,
            'wuxing': wuxing,
            'tiangan_wuxing': TIANGAN_WUXING[nagan_gan],
            'dizhi_wuxing': DIZHI_WUXING[nazhi_zhi],
        })

    return {
        'trigram': trigram_name,
        'nayi': result,
    }


def main():
    parser = argparse.ArgumentParser(description='纳甲纳支计算工具')
    parser.add_argument('--trigram', required=True, help='八卦名称（乾、坤、震、巽、坎、离、艮、兑）')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    try:
        result = calculate_nayi(args.trigram)
        result['status'] = 'success'
    except ValueError as e:
        result = {
            'status': 'error',
            'message': str(e)
        }

    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        if result['status'] == 'success':
            print(f"{result['trigram']}卦纳甲纳支：")
            print("爻位\t天干\t地支\t五行")
            print("-" * 30)
            for yao in result['nayi']:
                print(f"{yao['name']}\t{yao['tiangan']}\t{yao['dizhi']}\t{yao['wuxing']}")
        else:
            print(f"错误: {result['message']}")


if __name__ == '__main__':
    main()
