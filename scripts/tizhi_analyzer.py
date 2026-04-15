#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
体质分析脚本
根据输入的身体特征，分析体质类型
"""

import argparse
import json


# 八种体质特征
TIZHI_FEATURES = {
    '平和质': {
        'features': ['面色红润', '精力充沛', '睡眠良好', '食欲正常', '大便正常', '不易生病'],
        'trigram': '乾',
        'wuxing': '金',
        'description': '阴阳气血调和，体态适中，面色红润，精力充沛',
        'health_advice': '保持规律作息，适度运动，维持现有健康状态',
    },
    '气虚质': {
        'features': ['容易疲劳', '气短懒言', '容易出汗', '易感冒', '舌淡苔白'],
        'trigram': '坤',
        'wuxing': '土',
        'description': '元气不足，容易疲劳，气短懒言，容易出汗',
        'health_advice': '补气养血，适当休息，避免过度劳累',
    },
    '阳虚质': {
        'features': ['怕冷', '手脚冰凉', '喜热饮', '容易腹泻', '舌淡苔白'],
        'trigram': '坎',
        'wuxing': '水',
        'description': '阳气不足，怕冷，手脚冰凉，喜热饮',
        'health_advice': '温阳散寒，注意保暖，避免受凉',
    },
    '阴虚质': {
        'features': ['怕热', '口干咽燥', '容易心烦', '手足心热', '舌红少苔'],
        'trigram': '离',
        'wuxing': '火',
        'description': '阴液不足，怕热，口干咽燥，容易心烦',
        'health_advice': '滋阴降火，避免辛辣，多喝水',
    },
    '痰湿质': {
        'features': ['体型肥胖', '容易出汗', '口黏腻', '大便黏滞', '舌苔厚腻'],
        'trigram': '艮',
        'wuxing': '土',
        'description': '痰湿内盛，体型肥胖，容易出汗，口黏腻',
        'health_advice': '健脾祛湿，清淡饮食，适度运动',
    },
    '湿热质': {
        'features': ['容易长痘', '口苦口臭', '大便黏滞', '小便黄', '舌苔黄腻'],
        'trigram': '震',
        'wuxing': '木',
        'description': '湿热内蕴，容易长痘，口苦口臭，小便黄',
        'health_advice': '清热利湿，避免油腻，多喝绿茶',
    },
    '血瘀质': {
        'features': ['面色晦暗', '皮肤粗糙', '容易痛经', '舌质紫暗', '有瘀点'],
        'trigram': '巽',
        'wuxing': '木',
        'description': '血行不畅，面色晦暗，皮肤粗糙，容易痛经',
        'health_advice': '活血化瘀，适当运动，避免久坐',
    },
    '气郁质': {
        'features': ['情绪不稳', '容易抑郁', '胸闷叹息', '女性经前乳胀', '舌苔薄白'],
        'trigram': '兑',
        'wuxing': '金',
        'description': '气机郁滞，情绪不稳，容易抑郁，胸闷叹息',
        'health_advice': '疏肝解郁，保持心情舒畅，多社交',
    },
}


def analyze_tizhi(features):
    """
    分析体质类型

    参数:
    features: 身体特征列表，如 ['容易疲劳', '怕冷', '手脚冰凉']

    返回:
    体质类型和分析结果
    """
    if not features:
        return {
            'status': 'error',
            'message': '特征列表不能为空'
        }

    # 计算每种体质的匹配度
    scores = {}
    for tizhi, info in TIZHI_FEATURES.items():
        tizhi_features = set(info['features'])
        input_features = set(features)

        # 计算匹配度
        matched = len(input_features & tizhi_features)
        total = len(input_features)

        if total > 0:
            score = matched / total
        else:
            score = 0

        scores[tizhi] = score

    # 找出匹配度最高的体质
    max_score = max(scores.values())
    best_matches = [t for t, s in scores.items() if s == max_score]

    # 如果最高匹配度太低，返回平和质
    if max_score < 0.3:
        result_tizhi = '平和质'
        confidence = 0.5
    else:
        result_tizhi = best_matches[0]
        confidence = max_score

    result_info = TIZHI_FEATURES[result_tizhi]

    return {
        'status': 'success',
        'tizhi': result_tizhi,
        'confidence': round(confidence * 100, 2),
        'trigram': result_info['trigram'],
        'wuxing': result_info['wuxing'],
        'description': result_info['description'],
        'health_advice': result_info['health_advice'],
        'all_scores': {t: round(s * 100, 2) for t, s in scores.items()},
    }


def main():
    parser = argparse.ArgumentParser(description='体质分析工具')
    parser.add_argument('--features', required=True, help='身体特征，用逗号分隔。例如: 容易疲劳,怕冷,手脚冰凉')
    parser.add_argument('--format', default='json', choices=['json', 'text'], help='输出格式')

    args = parser.parse_args()

    try:
        # 解析特征
        features = [f.strip() for f in args.features.split(',')]

        # 分析体质
        result = analyze_tizhi(features)

        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 文本格式输出
            if result['status'] == 'success':
                print(f"体质分析结果")
                print(f"体质类型: {result['tizhi']}")
                print(f"置信度: {result['confidence']}%")
                print(f"对应八卦: {result['trigram']}（{result['wuxing']}）")
                print(f"描述: {result['description']}")
                print(f"养生建议: {result['health_advice']}")
                print()
                print("各体质匹配度:")
                for tizhi, score in result['all_scores'].items():
                    print(f"  {tizhi}: {score}%")
            else:
                print(f"错误: {result['message']}")

    except Exception as e:
        result = {
            'status': 'error',
            'message': str(e)
        }
        print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
