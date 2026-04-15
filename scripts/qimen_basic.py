#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲基础脚本
功能：天盘地盘人盘、八门九星、格局判断
"""

import argparse
import json
import datetime

# 天干
TIAN_GAN = ["戊", "己", "庚", "辛", "壬", "癸", "丁", "丙", "乙"]
# 地支
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# 九星
JIU_XING = ["天蓬", "天任", "天冲", "天辅", "天英", "天芮", "天柱", "天心", "天禽"]
# 八门
BA_MEN = ["休门", "死门", "伤门", "杜门", "中门", "开门", "惊门", "生门", "景门"]
# 八神
BA_SHEN = ["值符", "腾蛇", "太阴", "六合", "白虎", "玄武", "九地", "九天"]

# 九宫对应八卦
JIU_GONG_BAGUA = ["坎", "坤", "震", "巽", "中", "乾", "兑", "艮", "离"]

# 八门吉凶
MEN_JI_XIONG = {
    "开门": "吉", "休门": "吉", "生门": "吉",
    "伤门": "凶", "杜门": "凶", "景门": "凶",
    "死门": "大凶", "惊门": "凶"
}

# 九星五行
XING_WUXING = {
    "天蓬": "水", "天任": "土", "天冲": "木",
    "天辅": "木", "天英": "火", "天芮": "土",
    "天柱": "金", "天心": "金", "天禽": "土"
}

def get_jie_qi(year, month, day):
    """获取节气（简化版）"""
    # 节气日期（近似）
    jie_qi_dates = {
        1: 6,   # 小寒
        2: 4,   # 立春
        3: 6,   # 惊蛰
        4: 5,   # 清明
        5: 6,   # 立夏
        6: 6,   # 芒种
        7: 7,   # 小暑
        8: 8,   # 立秋
        9: 8,   # 白露
        10: 8,  # 寒露
        11: 7,  # 立冬
        12: 7   # 大雪
    }
    
    jie_qi_day = jie_qi_dates.get(month, 15)
    is_after_jieqi = day >= jie_qi_day
    
    # 节气对应的月建
    if is_after_jieqi:
        jie_qi_month = month
    else:
        jie_qi_month = month - 1 if month > 1 else 12
    
    return jie_qi_month, is_after_jieqi

def calculate_qimen(year=None, month=None, day=None, hour=None):
    """
    奇门遁甲排盘
    
    Args:
        year/month/day/hour: 公历时间
    
    Returns:
        奇门遁甲排盘结果
    """
    if year is None:
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
    
    result = {
        "time": f"{year}年{month}月{day}日{hour}时",
        "pan": {},
        "judgment": ""
    }
    
    # 1. 确定节气和月建
    jie_qi_month, is_after_jieqi = get_jie_qi(year, month, day)
    result["jie_qi"] = {
        "month": jie_qi_month,
        "is_after": is_after_jieqi
    }
    
    # 2. 确定时辰
    shichen = (hour + 1) // 2 % 12
    shichen_name = DI_ZHI[shichen]
    result["shichen"] = shichen_name
    
    # 3. 确定旬首（简化版，使用年月日时计算）
    # 实际奇门需要复杂的干支计算，这里使用简化逻辑
    
    # 4. 排天盘（九星）
    # 根据时辰和节气确定值符和天盘位置
    # 简化：根据时辰轮转九星
    xing_index = (shichen + jie_qi_month) % 9
    zhi_fu = JIU_XING[xing_index]
    
    # 天盘排列（以值符为中心，按固定顺序排列）
    tian_pan = {}
    for i, xing in enumerate(JIU_XING):
        gong = (xing_index + i) % 9
        tian_pan[gong] = xing
    
    result["pan"]["tian"] = tian_pan
    
    # 5. 排地盘（八门）
    # 根据时辰和节气确定值使和八门位置
    men_index = (shichen + jie_qi_month) % 8
    zhi_shi = BA_MEN[men_index]
    
    # 地盘排列
    di_pan = {}
    for i, men in enumerate(BA_MEN):
        gong = (men_index + i) % 9
        di_pan[gong] = men
    
    result["pan"]["di"] = di_pan
    
    # 6. 排人盘（八神）
    # 根据值符位置排八神
    shen_index = shichen % 8
    ren_pan = {}
    for i, shen in enumerate(BA_SHEN):
        gong = (shen_index + i) % 9
        ren_pan[gong] = shen
    
    result["pan"]["ren"] = ren_pan
    
    # 7. 格局判断
    # 分析吉凶
    ji_men_count = 0
    xiong_men_count = 0
    gong_analysis = []
    
    for gong in range(9):
        men = di_pan.get(gong, "")
        xing = tian_pan.get(gong, "")
        shen = ren_pan.get(gong, "")
        
        men_jx = MEN_JI_XIONG.get(men, "平")
        
        if men_jx in ["吉"]:
            ji_men_count += 1
        elif men_jx in ["凶", "大凶"]:
            xiong_men_count += 1
        
        gong_analysis.append({
            "gong": gong + 1,
            "bagua": JIU_GONG_BAGUA[gong],
            "men": men,
            "men_jx": men_jx,
            "xing": xing,
            "xing_wuxing": XING_WUXING.get(xing, ""),
            "shen": shen
        })
    
    result["gong_analysis"] = gong_analysis
    result["ji_men_count"] = ji_men_count
    result["xiong_men_count"] = xiong_men_count
    
    # 整体吉凶判断
    if ji_men_count >= 4:
        result["judgment"] = "吉"
        result["judgment_desc"] = f"吉门{ji_men_count}个，格局较好"
    elif xiong_men_count >= 4:
        result["judgment"] = "凶"
        result["judgment_desc"] = f"凶门{xiong_men_count}个，需谨慎"
    else:
        result["judgment"] = "中平"
        result["judgment_desc"] = f"吉凶各半，视具体方位"
    
    # 推荐方位
    recommended_directions = []
    for gong in gong_analysis:
        if gong["men_jx"] in ["吉"] and gong["shen"] not in ["白虎", "螣蛇"]:
            recommended_directions.append({
                "direction": gong["bagua"],
                "reason": f"{gong['men']}配{gong['xing']}"
            })
    
    result["recommended_directions"] = recommended_directions[:3]  # 最多推荐3个
    
    return result

def main():
    parser = argparse.ArgumentParser(description="奇门遁甲基础")
    parser.add_argument("--year", type=int, help="年份")
    parser.add_argument("--month", type=int, help="月份")
    parser.add_argument("--day", type=int, help="日期")
    parser.add_argument("--hour", type=int, help="时辰")
    parser.add_argument("--format", default="json", choices=["json", "text"], help="输出格式")
    
    args = parser.parse_args()
    
    # 计算奇门遁甲
    result = calculate_qimen(args.year, args.month, args.day, args.hour)
    
    # 输出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 70)
        print(f"【奇门遁甲】{result['time']}")
        print("=" * 70)
        print(f"\n节气：{result['jie_qi']['month']}月建（{'已过' if result['jie_qi']['is_after'] else '未过'}）")
        print(f"时辰：{result['shichen']}")
        
        print(f"\n【排盘】")
        for gong in result["gong_analysis"]:
            print(f"  {gong['gong']}宫（{gong['bagua']}）：{gong['men']}（{gong['men_jx']}） {gong['xing']} {gong['shen']}")
        
        print(f"\n【吉凶判断】")
        print(f"  {result['judgment']} - {result['judgment_desc']}")
        
        if result["recommended_directions"]:
            print(f"\n【推荐方位】")
            for dir_info in result["recommended_directions"]:
                print(f"  • {dir_info['direction']}：{dir_info['reason']}")
        
        print("=" * 70)

if __name__ == "__main__":
    main()
