#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脑区映射工具 - 卦象到脑区的对应关系
功能：前额叶、杏仁核、海马体等脑区与卦象的映射
"""

import argparse
import json

class BrainRegionMapper:
    """
    脑区与卦象映射器
    """
    
    def __init__(self):
        self.brain_regions = self._build_brain_regions()
        self.gua_mapping = self._build_gua_mapping()
    
    def _build_brain_regions(self):
        """
        构建脑区系统
        """
        return {
            "前额叶皮层": {
                "function": "决策、执行、计划",
                "yin_yang": "阳（主动）",
                "corresponding_gua": "乾卦"
            },
            "杏仁核": {
                "function": "情绪、恐惧、奖励",
                "yin_yang": "阴（情绪）",
                "corresponding_gua": "坎卦"
            },
            "海马体": {
                "function": "记忆、学习、空间导航",
                "yin_yang": "阴（存储）",
                "corresponding_gua": "艮卦"
            },
            "顶叶": {
                "function": "感知、空间、注意",
                "yin_yang": "阳（感知）",
                "corresponding_gua": "离卦"
            },
            "枕叶": {
                "function": "视觉处理",
                "yin_yang": "阳（视觉）",
                "corresponding_gua": "离卦"
            },
            "颞叶": {
                "function": "听觉、语言、记忆",
                "yin_yang": "阴阳混合",
                "corresponding_gua": "巽卦"
            },
            "小脑": {
                "function": "运动协调、平衡",
                "yin_yang": "阳（协调）",
                "corresponding_gua": "震卦"
            },
            "脑干": {
                "function": "生命维持（呼吸、心跳）",
                "yin_yang": "阴（基础）",
                "corresponding_gua": "坤卦"
            }
        }
    
    def _build_gua_mapping(self):
        """
        构建卦象映射
        """
        return {
            "乾卦": {
                "brain_region": "前额叶皮层",
                "function": "天行健，决策执行",
                "characteristics": ["刚健", "决断", "领导"]
            },
            "坤卦": {
                "brain_region": "脑干",
                "function": "厚德载物，生命维持",
                "characteristics": ["承载", "基础", "稳定"]
            },
            "坎卦": {
                "brain_region": "杏仁核",
                "function": "坎陷，情绪处理",
                "characteristics": ["情绪", "险陷", "恐惧"]
            },
            "离卦": {
                "brain_region": "顶叶/枕叶",
                "function": "离明，感知觉知",
                "characteristics": ["明亮", "感知", "觉知"]
            },
            "艮卦": {
                "brain_region": "海马体",
                "function": "艮止，记忆存储",
                "characteristics": ["静止", "记忆", "积累"]
            },
            "震卦": {
                "brain_region": "小脑",
                "function": "震动，运动协调",
                "characteristics": ["行动", "运动", "协调"]
            },
            "巽卦": {
                "brain_region": "颞叶",
                "function": "巽入，语言听觉",
                "characteristics": ["深入", "沟通", "学习"]
            },
            "兑卦": {
                "brain_region": "前额叶-杏仁核回路",
                "function": "兑悦，情感表达",
                "characteristics": ["愉悦", "表达", "交流"]
            }
        }
    
    def map_brain_network(self):
        """
        映射大脑网络
        """
        return {
            "默认模式网络": {
                "function": "自我参照、内在思维",
                "yin_yang": "阴（内在）",
                "gua": "坤卦"
            },
            "执行控制网络": {
                "function": "决策、规划、抑制",
                "yin_yang": "阳（执行）",
                "gua": "乾卦"
            },
            "显著性网络": {
                "function": "检测重要性、切换网络",
                "yin_yang": "阴阳平衡",
                "gua": "泰卦"
            },
            "情绪网络": {
                "function": "情绪处理、体验",
                "yin_yang": "阴（情绪）",
                "gua": "坎卦"
            },
            "视觉网络": {
                "function": "视觉处理",
                "yin_yang": "阳（视觉）",
                "gua": "离卦"
            }
        }
    
    def analyze_neurotransmitters(self):
        """
        分析神经递质与阴阳
        """
        return {
            "多巴胺": {
                "function": "奖励、动机、运动",
                "yin_yang": "阳（兴奋）",
                "imbalance": "过多 → 躁狂，过少 → 抑郁"
            },
            "血清素": {
                "function": "情绪、睡眠、食欲",
                "yin_yang": "阴（镇静）",
                "imbalance": "过多 → 嗜睡，过少 → 焦虑"
            },
            "去甲肾上腺素": {
                "function": "注意、觉醒",
                "yin_yang": "阳（激活）",
                "imbalance": "过多 → 焦虑，过少 → 嗜睡"
            },
            "GABA": {
                "function": "抑制、镇静",
                "yin_yang": "阴（抑制）",
                "imbalance": "不足 → 癫痫、焦虑"
            },
            "谷氨酸": {
                "function": "兴奋、学习",
                "yin_yang": "阳（兴奋）",
                "imbalance": "过多 → 兴奋毒性"
            }
        }
    
    def map_brain_states(self):
        """
        映射大脑状态
        """
        return {
            "清醒状态": {
                "yin_yang": "阳为主导",
                "gua": "乾卦",
                "characteristics": ["活跃", "意识", "决策"]
            },
            "睡眠状态": {
                "yin_yang": "阴为主导",
                "gua": "坤卦",
                "characteristics": ["休息", "恢复", "潜意识"]
            },
            "冥想状态": {
                "yin_yang": "阴阳平衡",
                "gua": "泰卦",
                "characteristics": ["平衡", "觉知", "宁静"]
            },
            "压力状态": {
                "yin_yang": "阳过盛",
                "gua": "大壮卦",
                "characteristics": ["紧张", "警觉", "应对"]
            },
            "抑郁状态": {
                "yin_yang": "阴过盛",
                "gua": "剥卦",
                "characteristics": ["低落", "迟缓", "退缩"]
            }
        }

def main():
    parser = argparse.ArgumentParser(description="脑区映射工具")
    parser.add_argument("--regions", action="store_true", help="脑区映射")
    parser.add_argument("--networks", action="store_true", help="大脑网络映射")
    parser.add_argument("--neurotransmitters", action="store_true", help="神经递质分析")
    parser.add_argument("--states", action="store_true", help="大脑状态映射")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    mapper = BrainRegionMapper()
    
    if args.regions:
        result = {
            "brain_regions": mapper.brain_regions,
            "gua_mapping": mapper.gua_mapping
        }
    elif args.networks:
        result = mapper.map_brain_network()
    elif args.neurotransmitters:
        result = mapper.analyze_neurotransmitters()
    elif args.states:
        result = mapper.map_brain_states()
    else:
        # 默认：脑区映射
        result = {
            "brain_regions": mapper.brain_regions,
            "gua_mapping": mapper.gua_mapping
        }
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print("【脑区与卦象映射】")
        print("=" * 70)
        
        if "brain_regions" in result:
            print(f"\n【脑区映射】")
            for region, info in result["brain_regions"].items():
                print(f"\n{region}:")
                print(f"  功能：{info['function']}")
                print(f"  阴阳：{info['yin_yang']}")
                print(f"  对应卦象：{info['corresponding_gua']}")
        
        elif "默认模式网络" in result:
            print(f"\n【大脑网络映射】")
            for network, info in result.items():
                print(f"\n{network}:")
                print(f"  功能：{info['function']}")
                print(f"  阴阳：{info['yin_yang']}")
                print(f"  对应卦象：{info['gua']}")
        
        elif "多巴胺" in result:
            print(f"\n【神经递质与阴阳】")
            for nt, info in result.items():
                print(f"\n{nt}:")
                print(f"  功能：{info['function']}")
                print(f"  阴阳：{info['yin_yang']}")
                print(f"  失衡：{info['imbalance']}")
        
        elif "清醒状态" in result:
            print(f"\n【大脑状态映射】")
            for state, info in result.items():
                print(f"\n{state}:")
                print(f"  阴阳：{info['yin_yang']}")
                print(f"  对应卦象：{info['gua']}")
                print(f"  特征：{', '.join(info['characteristics'])}")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
