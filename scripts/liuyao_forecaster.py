#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六爻预测脚本
根据摇卦结果和预测目的，进行六爻预测分析
"""

import argparse
import json
import sys


# 六亲定义
LIUQIN = {
    '父母': '生我者',
    '兄弟': '同我者',
    '子孙': '我生者',
    '妻财': '我克者',
    '官鬼': '克我者',
}

# 五行生克关系
WUXING_SHENG = {
    '木': '火',
    '火': '土',
    '土': '金',
    '金': '水',
    '水': '木',
}

WUXING_KE = {
    '木': '土',
    '土': '水',
    '水': '火',
    '火': '金',
    '金': '木',
}

# 预测目的对应的用神
PURPOSE_YONGSHEN = {
    '财运': '妻财',
    '官运': '官鬼',
    '学业': '父母',
    '婚姻': '妻财',  # 男测
    '婚姻_f': '官鬼',  # 女测
    '子女': '子孙',
    '健康': '官鬼',
    '生意': '妻财',
    '竞争': '兄弟',
    '出行': '子孙',
    '诉讼': '官鬼',
}

# 爻位名称
YAO_NAMES = ['初', '二', '三', '四', '五', '上']


def calculate_liuqin(shi_wuxing, yao_wuxing):
    """
    计算六亲关系

    参数:
    shi_wuxing: 世爻五行
    yao_wuxing: 某爻五行

    返回:
    六亲关系
    """
    # 父母：生我者
    if WUXING_SHENG.get(yao_wuxing) == shi_wuxing:
        return '父母'

    # 兄弟：同我者
    if yao_wuxing == shi_wuxing:
        return '兄弟'

    # 子孙：我生者
    if WUXING_SHENG.get(shi_wuxing) == yao_wuxing:
        return '子孙'

    # 妻财：我克者
    if WUXING_KE.get(shi_wuxing) == yao_wuxing:
        return '妻财'

    # 官鬼：克我者
    if WUXING_KE.get(yao_wuxing) == shi_wuxing:
        return '官鬼'

    return '未知'


def analyze_shengke(yao1_wuxing, yao2_wuxing):
    """
    分析两个爻的生克关系

    参数:
    yao1_wuxing: 爻1五行
    yao2_wuxing: 爻2五行

    返回:
    生克关系（生、克、被生、被克、同类）
    """
    # 同类
    if yao1_wuxing == yao2_wuxing:
        return '同类'

    # 生：yao1生yao2
    if WUXING_SHENG.get(yao1_wuxing) == yao2_wuxing:
        return '生'

    # 克：yao1克yao2
    if WUXING_KE.get(yao1_wuxing) == yao2_wuxing:
        return '克'

    # 被生：yao2生yao1
    if WUXING_SHENG.get(yao2_wuxing) == yao1_wuxing:
        return '被生'

    # 被克：yao2克yao1
    if WUXING_KE.get(yao2_wuxing) == yao1_wuxing:
        return '被克'

    return '未知'


def liuyao_forecast(yao_wuxing_list, shi_position, purpose):
    """
    六爻预测

    参数:
    yao_wuxing_list: 六爻五行列表，如 ['木', '火', '土', '金', '水', '木']
    shi_position: 世爻位置（1-6）
    purpose: 预测目的（财运、官运、学业、婚姻、子女、健康、生意、竞争、出行、诉讼）

    返回:
    预测结果
    """
    if len(yao_wuxing_list) != 6:
        raise ValueError("五行列表必须包含6个爻")

    if shi_position < 1 or shi_position > 6:
        raise ValueError("世爻位置必须在1-6之间")

    # 确定用神
    yongshen = PURPOSE_YONGSHEN.get(purpose, None)
    if yongshen is None:
        raise ValueError(f"未知预测目的: {purpose}")

    # 世爻五行
    shi_wuxing = yao_wuxing_list[shi_position - 1]

    # 应爻位置（世爻的对面）
    if shi_position <= 3:
        ying_position = shi_position + 3
    else:
        ying_position = shi_position - 3

    # 计算每一爻的六亲
    liuqin_list = []
    yongshen_positions = []  # 用神爻的位置

    for i, wuxing in enumerate(yao_wuxing_list):
        liuqin = calculate_liuqin(shi_wuxing, wuxing)
        position = i + 1

        liuqin_info = {
            'position': position,
            'name': YAO_NAMES[i],
            'wuxing': wuxing,
            'liuqin': liuqin,
        }

        # 标记世爻和应爻
        if position == shi_position:
            liuqin_info['role'] = '世爻'
        elif position == ying_position:
            liuqin_info['role'] = '应爻'

        # 标记用神爻
        if liuqin == yongshen:
            liuqin_info['is_yongshen'] = True
            yongshen_positions.append(position)
        else:
            liuqin_info['is_yongshen'] = False

        liuqin_list.append(liuqin_info)

    # 分析用神爻的状态
    yongshen_analysis = []
    for pos in yongshen_positions:
        yao = liuqin_list[pos - 1]
        yongshen_wuxing = yao['wuxing']

        # 世爻对用神爻的生克
        shi_relation = analyze_shengke(shi_wuxing, yongshen_wuxing)

        analysis = {
            'position': pos,
            'name': yao['name'],
            'wuxing': yongshen_wuxing,
            'shi_relation': shi_relation,
            'meaning': '',
        }

        # 解释生克含义
        if shi_relation == '生':
            analysis['meaning'] = '世爻生用神，自身付出，有利于发展'
        elif shi_relation == '克':
            analysis['meaning'] = '世爻克用神，自身有力，可获得结果'
        elif shi_relation == '被生':
            analysis['meaning'] = '用神生世爻，得外部支持，吉'
        elif shi_relation == '被克':
            analysis['meaning'] = '用神克世爻，受外部压力，不吉'
        elif shi_relation == '同类':
            analysis['meaning'] = '用神与世爻同类，中性'

        yongshen_analysis.append(analysis)

    # 综合判断
    if not yongshen_positions:
        overall_judgment = '卦中无用神爻，无法准确判断'
        overall_jixiong = '未知'
    else:
        # 简化判断：看世爻与用神的关系
        positive_relations = ['生', '被生', '同类']  # 吉
        negative_relations = ['克', '被克']  # 凶

        positive_count = sum(1 for a in yongshen_analysis if a['shi_relation'] in positive_relations)
        negative_count = sum(1 for a in yongshen_analysis if a['shi_relation'] in negative_relations)

        if positive_count > negative_count:
            overall_judgment = '总体吉利，用神得生或同类'
            overall_jixiong = '吉'
        elif negative_count > positive_count:
            overall_judgment = '总体不吉，用神受克'
            overall_jixiong = '凶'
        else:
            overall_judgment = '吉凶参半，需要结合其他因素'
            overall_jixiong = '参半'

    return {
        'status': 'success',
        'purpose': purpose,
        'yongshen': yongshen,
        'shi_position': shi_position,
        'shi_wuxing': shi_wuxing,
        'ying_position': ying_position,
        'liuqin': liuqin_list,
        'yongshen_analysis': yongshen_analysis,
        'overall_judgment': overall_judgment,
        'overall_jixiong': overall_jixiong,
    }


def main():
    parser = argparse.ArgumentParser(description='六爻预测工具')
    parser.add_argument('--wuxing', required=True, help='六爻五行列表，用逗号分隔。例如: 木,火,土,金,水,木')
    parser.add_argument('--shi', type=int, required=True, help='世爻位置（1-6）')
    parser.add_argument('--purpose', required=True, help='预测目的（财运、官运、学业、婚姻、子女、健康、生意、竞争、出行、诉讼）')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    try:
        # 解析五行列表
        wuxing_list = [w.strip() for w in args.wuxing.split(',')]
        if len(wuxing_list) != 6:
            raise ValueError("五行列表必须包含6个爻")

        # 六爻预测
        result = liuyao_forecast(wuxing_list, args.shi, args.purpose)

        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 文本格式输出
            print(f"六爻预测分析")
            print(f"预测目的: {result['purpose']}")
            print(f"用神: {result['yongshen']}")
            print(f"世爻: 第{result['shi_position']}位（{result['shi_wuxing']}）")
            print(f"应爻: 第{result['ying_position']}位")
            print()

            print("六爻详情:")
            print("爻位\t五行\t六亲\t角色")
            print("-" * 40)
            for yao in result['liuqin']:
                role = yao.get('role', '')
                yongshen_mark = ' [用神]' if yao.get('is_yongshen') else ''
                print(f"{yao['name']}\t{yao['wuxing']}\t{yao['liuqin']}\t{role}{yongshen_mark}")

            print()
            print("用神爻分析:")
            for analysis in result['yongshen_analysis']:
                print(f"  {analysis['name']}爻: {analysis['shi_relation']} - {analysis['meaning']}")

            print()
            print(f"综合判断: {result['overall_judgment']}（{result['overall_jixiong']}）")

    except ValueError as e:
        result = {
            'status': 'error',
            'message': str(e)
        }
        print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
