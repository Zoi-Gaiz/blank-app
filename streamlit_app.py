import streamlit as st

# --- 1. 页面基础配置 ---
st.set_page_config(page_title="洛克战术大师 Pro", page_icon="⚔️", layout="centered")

# --- 2. 属性图标与颜色定义 ---
# 模拟洛克王国官方色系与图标
TYPE_DATA = {
    "普通": {"icon": "⚪", "color": "#A8A878"},
    "草": {"icon": "🌿", "color": "#78C850"},
    "火": {"icon": "🔥", "color": "#F08030"},
    "水": {"icon": "💧", "color": "#6890F0"},
    "光": {"icon": "✨", "color": "#F8D030"},
    "地": {"icon": "⛰️", "color": "#E0C068"},
    "冰": {"icon": "❄️", "color": "#98D8D8"},
    "龙": {"icon": "🐲", "color": "#7038F8"},
    "电": {"icon": "⚡", "color": "#F8D030"},
    "毒": {"icon": "🟣", "color": "#A040A0"},
    "虫": {"icon": "🐞", "color": "#A8B820"},
    "武": {"icon": "🥊", "color": "#C03028"},
    "翼": {"icon": "🕊️", "color": "#A890F0"},
    "萌": {"icon": "🎀", "color": "#F85888"},
    "幽": {"icon": "👻", "color": "#705898"},
    "恶": {"icon": "🌙", "color": "#705848"},
    "机械": {"icon": "⚙️", "color": "#B8B8D0"},
    "幻": {"icon": "🔮", "color": "#E858D8"},
}

TYPES = list(TYPE_DATA.keys())

# 辅助函数：生成带图标的彩色文本
def type_label(t):
    return f"{TYPE_DATA[t]['icon']} {t}"

# --- 3. 核心克制数据 (保留之前的 RELATIONS 字典) ---
RELATIONS = {
    "草": {"水": 2.0, "地": 2.0, "光": 2.0, "火": 0.5, "草": 0.5, "毒": 0.5, "虫": 0.5, "翼": 0.5, "龙": 0.5, "机械": 0.5},
    "火": {"草": 2.0, "冰": 2.0, "虫": 2.0, "机械": 2.0, "火": 0.5, "水": 0.5, "地": 0.5, "龙": 0.5},
    "水": {"火": 2.0, "地": 2.0, "机械": 2.0, "草": 0.5, "水": 0.5, "冰": 0.5, "龙": 0.5},
    "光": {"幽": 2.0, "恶": 2.0, "草": 0.5, "冰": 0.5},
    "地": {"火": 2.0, "电": 2.0, "毒": 2.0, "草": 0.5, "地": 0.5, "虫": 0.5, "武": 0.5},
    "冰": {"草": 2.0, "地": 2.0, "龙": 2.0, "翼": 2.0, "火": 0.5, "水": 0.5, "冰": 0.5, "机械": 0.5},
    "龙": {"龙": 2.0, "机械": 0.5},
    "电": {"水": 2.0, "翼": 2.0, "草": 0.5, "地": 0.5, "龙": 0.5, "电": 0.5},
    "毒": {"草": 2.0, "萌": 2.0, "地": 0.5, "毒": 0.5, "幽": 0.5, "机械": 0.5},
    "虫": {"草": 2.0, "萌": 2.0, "幻": 2.0, "火": 0.5, "毒": 0.5, "武": 0.5, "翼": 0.5, "幽": 0.5, "恶": 0.5, "机械": 0.5},
    "武": {"普通": 2.0, "地": 2.0, "冰": 2.0, "毒": 0.5, "虫": 0.5, "翼": 0.5, "萌": 0.5, "幽": 0.5, "恶": 0.5, "机械": 0.5},
    "翼": {"草": 2.0, "虫": 2.0, "武": 2.0, "地": 0.5, "电": 0.5, "龙": 0.5, "机械": 0.5},
    "萌": {"武": 2.0, "毒": 2.0, "火": 0.5, "萌": 0.5, "恶": 0.5, "机械": 0.5},
    "幽": {"萌": 2.0, "幽": 2.0, "幻": 2.0, "普通": 0.5, "恶": 0.5},
    "恶": {"萌": 2.0, "幽": 2.0, "地": 0.5, "武": 0.5, "恶": 0.5},
    "机械": {"冰": 2.0, "萌": 2.0, "火": 0.5, "水": 0.5, "地": 0.5, "电": 0.5, "机械": 0.5},
    "幻": {"毒": 2.0, "武": 2.0, "地": 0.5, "机械": 0.5, "幻": 0.5},
    "普通": {"地": 0.5, "幽": 0.5, "机械": 0.5}
}

def get_mult(atk, dfn):
    return RELATIONS.get(atk, {}).get(dfn, 1.0)

# --- 4. 界面布局 ---
st.title("🛡️ 洛克战术分析 Pro")

tab_def, tab_atk = st.tabs(["🛡️ 防御扫描", "⚔️ 打击覆盖"])

# --- 防御模式 ---
with tab_def:
    st.markdown("##### 🔍 扫描全队共同天敌")
    team_data = []
    for i in range(6):
        with st.expander(f"精灵 #{i+1} 属性配置", expanded=(i == 0)):
            # 这里增加了图标显示
            selected = st.pills(
                "点选属性", 
                TYPES, 
                format_func=lambda x: f"{TYPE_DATA[x]['icon']} {x}",
                key=f"def_p_v_{i}", 
                selection_mode="multi"
            )
            if len(selected) > 2:
                selected = selected[:2]
            team_data.append(selected if selected else ["普通"])

    if st.button("🚀 启动防御分析", type="primary"):
        gaps = []
        for enemy_atk in TYPES:
            best_def = min([1.0 * get_mult(enemy_atk, s[0]) * (get_mult(enemy_atk, s[1]) if len(s)>1 else 1.0) for s in team_data])
            if best_def >= 2.0:
                gaps.append((enemy_atk, best_def))

        if gaps:
            st.error("### ⚠️ 发现联防死角")
            for g, v in gaps:
                st.markdown(f":{TYPE_DATA[g]['color'].replace('#','')}[**{TYPE_DATA[g]['icon']} {g}系攻击**]：全队均会被克制 (受损 {v}x)")
        else:
            st.success("### ✅ 联防稳固！")

# --- 打击模式 ---
with tab_atk:
    st.markdown("##### 🎯 扫描打击盲点与补位建议")
    all_skills = st.pills(
        "选择全队已拥有的技能属性", 
        TYPES, 
        format_func=lambda x: f"{TYPE_DATA[x]['icon']} {x}",
        selection_mode="multi", 
        key="atk_p_v_main"
    )

    if st.button("🔥 启动打击分析", type="primary"):
        if not all_skills:
            st.error("请先选择技能属性！")
        else:
            uncovered = [t for t in TYPES if not any(get_mult(s, t) >= 2.0 for s in all_skills)]
            
            if not uncovered:
                st.success("### 🔥 完美打击面！已克制所有属性。")
            else:
                st.error(f"### ❄️ 打击盲点 ({len(uncovered)})")
                st.markdown("无法克制敌人：")
                # 彩色显示盲点
                cols = st.columns(4)
                for i, t in enumerate(uncovered):
                    cols[i % 4].markdown(f"**{TYPE_DATA[t]['icon']} {t}**")
                
                # 智能建议
                recommendations = []
                for potential_atk in TYPES:
                    newly_covered = [t for t in uncovered if get_mult(potential_atk, t) >= 2.0]
                    if newly_covered:
                        recommendations.append((potential_atk, newly_covered))
                
                recommendations.sort(key=lambda x: len(x[1]), reverse=True)
                
                if recommendations:
                    st.divider()
                    st.subheader("💡 补位方案建议")
                    for attr, targets in recommendations[:3]:
                        with st.status(f"方案：增加【{TYPE_DATA[attr]['icon']} {attr}系】技能/精灵", expanded=True):
                            st.write(f"可额外克制：{' 、'.join([type_label(t) for t in targets])}")
                            st.write(f"收益：新增 **{len(targets)}** 个克制面")
                else:
                    st.warning("暂无单一属性可有效补齐盲点。")

st.divider()
st.caption("Tip: 手机端建议直接点击图标操作，配色参考洛克王国属性系统。")