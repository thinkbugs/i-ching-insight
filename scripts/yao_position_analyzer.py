#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爻位深度解析脚本
功能：分析六爻的乘承比应关系、中正当位、得位失位、吉凶悔吝
"""

import argparse
import json

# 五行列表
WUXING_NAMES = ["金", "木", "水", "火", "土"]

# 阴阳属性（0=阴, 1=阳）
YIN_YANG_NAMES = ["阴", "阳"]

# 爻位名称
YAO_POSITION_NAMES = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"]

# 天干地支十神（用于六亲关系参考）
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def analyze_yao_position(yao_list):
    """
    分析爻位的乘承比应关系、中正当位等
    
    Args:
        yao_list: 六爻列表 [0,1,0,0,1,1]，0=阴，1=阳
    
    Returns:
        dict: 每个爻的详细分析
    """
    if len(yao_list) != 6:
        return {"error": "必须提供6个爻"}
    
    result = {
        "hexagram": {
            "yao": yao_list,
            "binary": "".join(map(str, yao_list)),
            "description": f"{''.join(['☰' if y==1 else '☷' for y in yao_list[:3]])}{''.join(['☰' if y==1 else '☷' for y in yao_list[3:]])}"
        },
        "yao_analysis": []
    }
    
    for i, yao in enumerate(yao_list):
        analysis = {
            "position": i + 1,
            "position_name": YAO_POSITION_NAMES[i],
            "yao_type": YIN_YANG_NAMES[yao],
            "is_yang": yao == 1,
            "is_yin": yao == 0
        }
        
        # === 1. 乘承分析 ===
        # 乘：上爻乘下爻（上爻对下爻的压力）
        # 承：下爻承上爻（下爻对上爻的支撑）
        
        analysis["cheng"] = None  # 乘关系
        analysis["cheng_details"] = []
        
        if i > 0:
            # 检查上爻是否乘本爻（上爻对下爻的乘）
            above_yao = yao_list[i-1]
            if above_yao != yao:  # 异性相乘
                analysis["cheng"] = {
                    "from": YAO_POSITION_NAMES[i-1],
                    "to": YAO_POSITION_NAMES[i],
                    "type": "乘",
                    "nature": "乘势压制" if above_yao == 1 else "柔乘刚",
                    "meaning": f"{YAO_POSITION_NAMES[i-1]}乘{YAO_POSITION_NAMES[i]}，{'刚乘柔' if above_yao == 1 else '柔乘刚'}"
                }
                analysis["cheng_details"].append(analysis["cheng"]["meaning"])
        
        analysis["cheng"] = None  # 承关系
        analysis["cheng_details"] = []
        
        if i < 5:
            # 检查本爻是否承上爻（下爻对上爻的承）
            above_yao = yao_list[i+1]
            if above_yao != yao:  # 异性相承
                analysis["cheng"] = {
                    "from": YAO_POSITION_NAMES[i],
                    "to": YAO_POSITION_NAMES[i+1],
                    "type": "承",
                    "nature": "顺承支撑" if above_yao == 1 else "柔承刚",
                    "meaning": f"{YAO_POSITION_NAMES[i]}承{YAO_POSITION_NAMES[i+1]}，{'柔承刚' if yao == 0 else '刚承柔'}"
                }
                analysis["cheng_details"].append(analysis["cheng"]["meaning"])
        
        # === 2. 比应分析 ===
        # 比：相邻爻的关系
        # 应：隔位相应（1-4, 2-5, 3-6）
        
        analysis["bi"] = []
        analysis["ying"] = None
        
        # 比关系（相邻）
        if i > 0:
            left_yao = yao_list[i-1]
            bi_type = "相比" if left_yao == yao else "相异"
            analysis["bi"].append({
                "position": YAO_POSITION_NAMES[i-1],
                "type": bi_type,
                "nature": "同气连枝" if left_yao == yao else "阴阳相济"
            })
        
        if i < 5:
            right_yao = yao_list[i+1]
            bi_type = "相比" if right_yao == yao else "相异"
            analysis["bi"].append({
                "position": YAO_POSITION_NAMES[i+1],
                "type": bi_type,
                "nature": "同气连枝" if right_yao == yao else "阴阳相济"
            })
        
        # 应关系（隔位）
        if i < 3:
            # 初应四(0-3), 二应五(1-4), 三应上(2-5)
            ying_pos = i + 3
            ying_yao = yao_list[ying_pos]
            if ying_yao != yao:  # 阴阳相应
                analysis["ying"] = {
                    "position": YAO_POSITION_NAMES[ying_pos],
                    "type": "相应",
                    "nature": "阴阳感应",
                    "meaning": f"{YAO_POSITION_NAMES[i]}与{YAO_POSITION_NAMES[ying_pos]}相应，阴阳相吸"
                }
            else:
                analysis["ying"] = {
                    "position": YAO_POSITION_NAMES[ying_pos],
                    "type": "不相应",
                    "nature": "同性相斥",
                    "meaning": f"{YAO_POSITION_NAMES[i]}与{YAO_POSITION_NAMES[ying_pos]}不相应，同性相斥"
                }
        
        # === 3. 中正当位分析 ===
        # 中位：二爻、五爻
        # 正位：阳爻在奇数位(1,3,5)，阴爻在偶数位(2,4,6)
        
        analysis["zhong"] = (i == 1 or i == 4)  # 二爻、五爻为中位
        analysis["zhong_name"] = YAO_POSITION_NAMES[i] if analysis["zhong"] else ""
        
        analysis["zheng"] = (yao == (i % 2))  # 阳爻在奇数位，阴爻在偶数位
        analysis["zheng_name"] = "得位" if analysis["zheng"] else "失位"
        
        analysis["zhong_zheng"] = analysis["zhong"] and analysis["zheng"]
        analysis["zhong_zheng_name"] = "中正" if analysis["zhong_zheng"] else ""
        analysis["zhong_zheng_meaning"] = ""
        
        if analysis["zhong_zheng"]:
            if i == 1:
                analysis["zhong_zheng_meaning"] = "二爻中正，得中得位，柔中"
            else:  # i == 4, 五爻
                analysis["zhong_zheng_meaning"] = "五爻中正，得中得位，刚中"
        elif analysis["zhong"]:
            analysis["zhong_zheng_meaning"] = f"{YAO_POSITION_NAMES[i]}得中但失位"
        elif analysis["zheng"]:
            analysis["zhong_zheng_meaning"] = f"{YAO_POSITION_NAMES[i]}得位但失中"
        else:
            analysis["zhong_zheng_meaning"] = f"{YAO_POSITION_NAMES[i]}失中失位"
        
        # === 4. 吉凶悔吝判断 ===
        # 基于爻位关系综合判断
        
        analysis["judgment"] = determine_judgment(analysis, i, yao)
        
        result["yao_analysis"].append(analysis)
    
    # 整体卦象分析
    result["overall"] = analyze_overall(result["yao_analysis"])
    
    return result

def determine_judgment(yao_analysis, position, is_yang):
    """
    基于爻位关系判断吉凶悔吝
    """
    judgment = {
        "result": "中平",  # 默认
        "factors": [],
        "reasoning": ""
    }
    
    positive_factors = []
    negative_factors = []
    
    # 1. 中正当位加分
    if yao_analysis.get("zhong_zheng"):
        positive_factors.append("中正当位")
    
    # 2. 阴阳相应加分
    if yao_analysis.get("ying") and yao_analysis["ying"]["type"] == "相应":
        positive_factors.append("阴阳相应")
    
    # 3. 乘承关系判断
    # 柔乘刚（阴乘阳）不利
    if position > 0 and yao_analysis.get("cheng"):
        if yao_analysis["cheng"]["type"] == "乘" and yao_analysis["cheng"]["nature"] == "柔乘刚":
            negative_factors.append("柔乘刚")
    
    # 4. 失中失位减分
    if not yao_analysis.get("zhong") and not yao_analysis.get("zheng"):
        negative_factors.append("失中失位")
    
    # 5. 五爻阳爻特别有利（九五至尊）
    if position == 4 and is_yang:
        positive_factors.append("九五至尊")
    
    # 6. 二爻阴爻特别有利（六二柔中）
    if position == 1 and not is_yang:
        positive_factors.append("六二柔中")
    
    # 综合判断
    judgment["factors"] = positive_factors + negative_factors
    judgment["positive_factors"] = positive_factors
    judgment["negative_factors"] = negative_factors
    
    # 评分
    score = len(positive_factors) - len(negative_factors)
    
    if score >= 2:
        judgment["result"] = "吉"
        judgment["reasoning"] = "，".join(positive_factors) + "，吉"
    elif score == 1:
        judgment["result"] = "小吉"
        judgment["reasoning"] = "，".join(positive_factors) + "，小吉"
    elif score == 0:
        if len(negative_factors) > 0:
            judgment["result"] = "悔"
            judgment["reasoning"] = "，".join(negative_factors) + "，悔"
        else:
            judgment["result"] = "中平"
            judgment["reasoning"] = "无特殊因素，中平"
    elif score == -1:
        judgment["result"] = "吝"
        judgment["reasoning"] = "，".join(negative_factors) + "，吝"
    else:
        judgment["result"] = "凶"
        judgment["reasoning"] = "，".join(negative_factors) + "，凶"
    
    return judgment

def analyze_overall(yao_analysis_list):
    """
    整体卦象分析
    """
    overall = {
        "zhong_zheng_count": 0,
        "ying_pairs": 0,
        "general_judgment": "",
        "key_points": []
    }
    
    # 统计中正当位
    for yao in yao_analysis_list:
        if yao.get("zhong_zheng"):
            overall["zhong_zheng_count"] += 1
    
    # 统计相应
    checked = set()
    for i, yao in enumerate(yao_analysis_list):
        if i < 3 and yao.get("ying") and yao["ying"]["type"] == "相应":
            ying_pos = i + 3
            if i not in checked and ying_pos not in checked:
                overall["ying_pairs"] += 1
                checked.add(i)
                checked.add(ying_pos)
    
    # 整体判断
    if overall["zhong_zheng_count"] >= 2:
        overall["general_judgment"] = "卦象中正，结构稳固"
        overall["key_points"].append(f"中正当位爻数：{overall['zhong_zheng_count']}")
    elif overall["zhong_zheng_count"] == 1:
        overall["general_judgment"] = "卦象基本中正"
        overall["key_points"].append(f"中正当位爻数：{overall['zhong_zheng_count']}")
    else:
        overall["general_judgment"] = "卦象失中失位，不够稳固"
    
    if overall["ying_pairs"] >= 2:
        overall["general_judgment"] += "，阴阳相应和谐"
        overall["key_points"].append(f"相应爻对数：{overall['ying_pairs']}")
    elif overall["ying_pairs"] == 1:
        overall["general_judgment"] += "，有相应之爻"
        overall["key_points"].append(f"相应爻对数：{overall['ying_pairs']}")
    else:
        overall["general_judgment"] += "，缺乏相应"
        overall["key_points"].append("相应爻对数：0")
    
    return overall

def main():
    parser = argparse.ArgumentParser(description="爻位深度解析")
    parser.add_argument("--yao", required=True, help="六爻列表，用逗号分隔（0=阴，1=阳），例如：0,0,1,0,1,1")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 解析爻列表
    try:
        yao_list = [int(y.strip()) for y in args.yao.split(",")]
        if len(yao_list) != 6:
            raise ValueError("必须提供6个爻")
        if any(y not in [0, 1] for y in yao_list):
            raise ValueError("爻值必须是0或1")
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return
    
    # 分析爻位
    result = analyze_yao_position(yao_list)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        print("=" * 60)
        print(f"卦象：{result['hexagram']['description']}")
        print(f"二进制：{result['hexagram']['binary']}")
        print("=" * 60)
        print("\n【爻位分析】\n")
        
        for i, yao in enumerate(result["yao_analysis"]):
            print(f"{yao['position_name']}（{yao['yao_type']}爻）")
            print(f"  中位：{'是' if yao['zhong'] else '否'}")
            print(f"  正位：{yao['zheng_name']}")
            print(f"  中正：{yao['zhong_zheng_meaning']}")
            
            if yao.get("ying"):
                print(f"  应：{yao['ying']['meaning']}")
            
            if yao.get("bi"):
                bi_str = "、".join([f"{b['position']}{b['nature']}" for b in yao['bi']])
                print(f"  比：{bi_str}")
            
            print(f"  吉凶判断：{yao['judgment']['result']} - {yao['judgment']['reasoning']}")
            print()
        
        print("=" * 60)
        print("【整体分析】")
        print(f"{result['overall']['general_judgment']}")
        for point in result['overall']['key_points']:
            print(f"  • {point}")
        print("=" * 60)

if __name__ == "__main__":
    main()
