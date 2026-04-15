#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卦象计算脚本
根据六爻的阴阳状态，计算卦象、错卦、综卦、互卦、变卦
"""

import argparse
import json


# 八卦定义
TRIGRAMS = {
    '000': {'name': '坤', 'symbol': '☷', 'nature': '地', 'wuxing': '土'},
    '001': {'name': '震', 'symbol': '☳', 'nature': '雷', 'wuxing': '木'},
    '010': {'name': '坎', 'symbol': '☵', 'nature': '水', 'wuxing': '水'},
    '011': {'name': '兑', 'symbol': '☱', 'nature': '泽', 'wuxing': '金'},
    '100': {'name': '艮', 'symbol': '☶', 'nature': '山', 'wuxing': '土'},
    '101': {'name': '离', 'symbol': '☲', 'nature': '火', 'wuxing': '火'},
    '110': {'name': '巽', 'symbol': '☴', 'nature': '风', 'wuxing': '木'},
    '111': {'name': '乾', 'symbol': '☰', 'nature': '天', 'wuxing': '金'},
}

# 64卦名称映射
HEXAGRAM_NAMES = {
    '000000': {'name': '坤', 'index': 2},
    '000001': {'name': '剥', 'index': 23},
    '000010': {'name': '比', 'index': 8},
    '000011': {'name': '观', 'index': 20},
    '000100': {'name': '豫', 'index': 16},
    '000101': {'name': '晋', 'index': 35},
    '000110': {'name': '萃', 'index': 45},
    '000111': {'name': '否', 'index': 12},
    '001000': {'name': '复', 'index': 24},
    '001001': {'name': '颐', 'index': 27},
    '001010': {'name': '屯', 'index': 3},
    '001011': {'name': '益', 'index': 42},
    '001100': {'name': '震', 'index': 51},
    '001101': {'name': '噬嗑', 'index': 21},
    '001110': {'name': '随', 'index': 17},
    '001111': {'name': '无妄', 'index': 25},
    '010000': {'name': '师', 'index': 7},
    '010001': {'name': '蒙', 'index': 4},
    '010010': {'name': '坎', 'index': 29},
    '010011': {'name': '涣', 'index': 59},
    '010100': {'name': '解', 'index': 40},
    '010101': {'name': '未济', 'index': 64},
    '010110': {'name': '困', 'index': 47},
    '010111': {'name': '讼', 'index': 6},
    '011000': {'name': '明夷', 'index': 36},
    '011001': {'name': '贲', 'index': 22},
    '011010': {'name': '既济', 'index': 63},
    '011011': {'name': '家人', 'index': 37},
    '011100': {'name': '丰', 'index': 55},
    '011101': {'name': '离', 'index': 30},
    '011110': {'name': '革', 'index': 49},
    '011111': {'name': '同人', 'index': 13},
    '100000': {'name': '谦', 'index': 15},
    '100001': {'name': '艮', 'index': 52},
    '100010': {'name': '蹇', 'index': 39},
    '100011': {'name': '渐', 'index': 53},
    '100100': {'name': '小过', 'index': 62},
    '100101': {'name': '旅', 'index': 56},
    '100110': {'name': '咸', 'index': 31},
    '100111': {'name': '遁', 'index': 33},
    '101000': {'name': '升', 'index': 46},
    '101001': {'name': '蛊', 'index': 18},
    '101010': {'name': '井', 'index': 48},
    '101011': {'name': '巽', 'index': 57},
    '101100': {'name': '恒', 'index': 32},
    '101101': {'name': '鼎', 'index': 50},
    '101110': {'name': '大过', 'index': 28},
    '101111': {'name': '姤', 'index': 44},
    '110000': {'name': '泰', 'index': 11},
    '110001': {'name': '大畜', 'index': 26},
    '110010': {'name': '需', 'index': 5},
    '110011': {'name': '小畜', 'index': 9},
    '110100': {'name': '大壮', 'index': 34},
    '110101': {'name': '大有', 'index': 14},
    '110110': {'name': '夬', 'index': 43},
    '110111': {'name': '履', 'index': 10},
    '111000': {'name': '临', 'index': 19},
    '111001': {'name': '损', 'index': 41},
    '111010': {'name': '节', 'index': 60},
    '111011': {'name': '中孚', 'index': 61},
    '111100': {'name': '归妹', 'index': 54},
    '111101': {'name': '睽', 'index': 38},
    '111110': {'name': '兑', 'index': 58},
    '111111': {'name': '乾', 'index': 1},
}


def binary_to_trigram(binary_str):
    """将三位二进制转换为八卦"""
    return TRIGRAMS.get(binary_str, None)


def calculate_hexagram(yao_list):
    """
    计算卦象
    yao_list: 六爻列表，0表示阴爻，1表示阳爻
    例如: [0, 0, 1, 0, 1, 1] 表示阴阳阳阴阳阴
    """
    if len(yao_list) != 6:
        raise ValueError("爻列表必须包含6个爻")

    # 转换为二进制字符串（初爻在最低位）
    binary_str = ''.join(str(y) for y in yao_list)

    # 上卦：三四五爻（索引3,4,5，注意顺序是自下而上）
    upper_binary = binary_str[3:6]
    upper_trigram = binary_to_trigram(upper_binary)

    # 下卦：初二三爻（索引0,1,2）
    lower_binary = binary_str[0:3]
    lower_trigram = binary_to_trigram(lower_binary)

    # 卦象符号
    symbol = f"{lower_trigram['symbol']}{upper_trigram['symbol']}"

    # 卦名
    hexagram_info = HEXAGRAM_NAMES.get(binary_str, {'name': '未知', 'index': 0})

    return {
        'binary': binary_str,
        'symbol': symbol,
        'name': hexagram_info['name'],
        'index': hexagram_info['index'],
        'upper_trigram': upper_trigram,
        'lower_trigram': lower_trigram,
        'upper_binary': upper_binary,
        'lower_binary': lower_binary,
    }


def calculate_cuo_gua(yao_list):
    """
    计算错卦（将所有爻的阴阳反转）
    """
    cuo_yao = [1 - y for y in yao_list]
    return calculate_hexagram(cuo_yao)


def calculate_zong_gua(yao_list):
    """
    计算综卦（将六爻上下颠倒）
    """
    zong_yao = yao_list[::-1]
    return calculate_hexagram(zong_yao)


def calculate_hu_gua(yao_list):
    """
    计算互卦（取二三四爻为下卦，三四五爻为上卦）
    """
    # 下卦：二三爻（索引1,2）+ 三爻的重复（索引2）？
    # 实际上互卦的规则是：二三四爻组成下卦，三四五爻组成上卦
    # 注意：爻位从下往上，所以索引顺序是：初(0), 二(1), 三(2), 四(3), 五(4), 上(5)
    # 二三四爻 = yao_list[1:4]
    # 三四五爻 = yao_list[2:5]

    # 下卦：二三爻（索引1,2）需要一个额外的爻来补成三位
    # 通常的做法是：下卦取二三爻 + 三爻重复？不对，应该取二三四爻
    # 让我重新理解：互卦是取中间四爻，二三爻和三四五爻各取三位形成上下卦
    # 下卦：二三四爻 = yao_list[1:4]
    # 上卦：三四五爻 = yao_list[2:5]

    hu_lower = yao_list[1:4]  # 二三四爻
    hu_upper = yao_list[2:5]  # 三四五爻

    return {
        'hu_lower': hu_lower,
        'hu_upper': hu_upper,
        'hu_gua': {
            'lower_trigram': binary_to_trigram(''.join(str(y) for y in hu_lower)),
            'upper_trigram': binary_to_trigram(''.join(str(y) for y in hu_upper)),
        }
    }


def calculate_bian_gua(yao_list, moving_lines=None):
    """
    计算变卦（动爻变化后形成的新卦）
    moving_lines: 动爻列表，索引从0开始（0表示初爻）
    """
    if moving_lines is None:
        moving_lines = []

    bian_yao = yao_list.copy()
    for line_idx in moving_lines:
        if 0 <= line_idx < 6:
            bian_yao[line_idx] = 1 - bian_yao[line_idx]

    return calculate_hexagram(bian_yao)


def main():
    parser = argparse.ArgumentParser(description='卦象计算工具')
    parser.add_argument('--yao', required=True, help='六爻列表，用逗号分隔，0表示阴爻，1表示阳爻。例如: 0,0,1,0,1,1')
    parser.add_argument('--moving', help='动爻列表，用逗号分隔，索引从0开始。例如: 0,2 表示初爻和三爻动')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    # 解析爻位
    try:
        yao_list = [int(y.strip()) for y in args.yao.split(',')]
        if len(yao_list) != 6:
            raise ValueError("爻列表必须包含6个爻")
        if any(y not in [0, 1] for y in yao_list):
            raise ValueError("爻只能是0（阴）或1（阳）")
    except ValueError as e:
        result = {
            'status': 'error',
            'message': f'爻位解析错误: {str(e)}'
        }
        print(json.dumps(result, ensure_ascii=False))
        return

    # 解析动爻
    moving_lines = []
    if args.moving:
        try:
            moving_lines = [int(m.strip()) for m in args.moving.split(',')]
            if any(m < 0 or m >= 6 for m in moving_lines):
                raise ValueError("动爻索引必须在0-5之间")
        except ValueError as e:
            result = {
                'status': 'error',
                'message': f'动爻解析错误: {str(e)}'
            }
            print(json.dumps(result, ensure_ascii=False))
            return

    # 计算各种卦象
    ben_gua = calculate_hexagram(yao_list)
    cuo_gua = calculate_cuo_gua(yao_list)
    zong_gua = calculate_zong_gua(yao_list)
    hu_gua = calculate_hu_gua(yao_list)
    bian_gua = calculate_bian_gua(yao_list, moving_lines)

    # 构建结果
    result = {
        'status': 'success',
        'ben_gua': {
            'name': ben_gua['name'],
            'index': ben_gua['index'],
            'symbol': ben_gua['symbol'],
            'yao': yao_list,
            'upper_trigram': ben_gua['upper_trigram']['name'],
            'lower_trigram': ben_gua['lower_trigram']['name'],
        },
        'cuo_gua': {
            'name': cuo_gua['name'],
            'index': cuo_gua['index'],
            'symbol': cuo_gua['symbol'],
            'meaning': '阴阳全反，镜像关系'
        },
        'zong_gua': {
            'name': zong_gua['name'],
            'index': zong_gua['index'],
            'symbol': zong_gua['symbol'],
            'meaning': '上下颠倒，视角转换'
        },
        'hu_gua': {
            'lower_trigram': hu_gua['hu_gua']['lower_trigram']['name'],
            'upper_trigram': hu_gua['hu_gua']['upper_trigram']['name'],
            'symbol': f"{hu_gua['hu_gua']['lower_trigram']['symbol']}{hu_gua['hu_gua']['upper_trigram']['symbol']}",
            'meaning': '内部结构，深层原因'
        },
        'bian_gua': {
            'name': bian_gua['name'],
            'index': bian_gua['index'],
            'symbol': bian_gua['symbol'],
            'moving_lines': moving_lines,
            'meaning': '动爻变化后形成的新卦'
        } if moving_lines else None,
    }

    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        print(f"本卦：{ben_gua['name']}卦 ({ben_gua['symbol']}) - 第{ben_gua['index']}卦")
        print(f"  上卦：{ben_gua['upper_trigram']}")
        print(f"  下卦：{ben_gua['lower_trigram']}")
        print(f"错卦：{cuo_gua['name']}卦 ({cuo_gua['symbol']}) - {cuo_gua['meaning']}")
        print(f"综卦：{zong_gua['name']}卦 ({zong_gua['symbol']}) - {zong_gua['meaning']}")
        print(f"互卦：{hu_gua['lower_trigram']}{hu_gua['upper_trigram']} ({hu_gua['symbol']}) - {hu_gua['meaning']}")
        if moving_lines:
            print(f"变卦：{bian_gua['name']}卦 ({bian_gua['symbol']}) - 动爻: {moving_lines}")


if __name__ == '__main__':
    main()
