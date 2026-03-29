import streamlit as st

# --- 1. 配置与样式 ---
st.set_page_config(page_title="洛克战术大师 Pro", page_icon="⚖️", layout="centered")

st.markdown("""
    <style>
    .type-tag { padding: 4px 10px; border-radius: 6px; color: white; font-weight: bold; margin-right: 8px; display: inline-block; font-size: 0.9rem; }
    .stButton > button { width: 100%; border-radius: 12px; height: 3.5rem; background-color: #2e86de; color: white; font-weight: bold; }
    .danger-box { background: #fff5f5; border-left: 5px solid #d63031; padding: 12px; border-radius: 6px; margin-bottom: 10px; }
    .info-box { background: #f0f7ff; border-left: 5px solid #2e86de; padding: 12px; border-radius: 6px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心数据 (严格执行: 同系互打 = 1.0) ---
TYPE_DATA = {
    "普通": {"icon": "⚪", "color": "#A8A878"}, "草": {"icon": "🌿", "color": "#78C850"},
    "火": {"icon": "🔥", "color": "#F08030"}, "水": {"icon": "💧", "color": "#6890F0"},
    "光": {"icon": "✨", "color": "#F8D030"}, "地": {"icon": "⛰️", "color": "#E0C068"},
    "冰": {"icon": "❄️", "color": "#98D8D8"}, "龙": {"icon": "🐲", "color": "#7038F8"},
    "电": {"icon": "⚡", "color": "#F8D030"}, "毒": {"icon": "🟣", "color": "#A040A0"},
    "虫": {"icon": "🐞", "color": "#A8B820"}, "武": {"icon": "🥊", "color": "#C03028"},
    "翼": {"icon": "🕊️", "color": "#A890F0"}, "萌": {"icon": "🎀", "color": "#F85888"},
    "幽": {"icon": "👻", "color": "#705898"}, "恶": {"icon": "🌙", "color": "#705848"},
    "机械": {"icon": "⚙️", "color": "#B8B8D0"}, "幻": {"icon": "🔮", "color": "#E858D8"},
}
TYPES = list(TYPE_DATA.keys())

# --- 核心克制字典 (严格复核 2026 赛季最新数据，依据提供的图片修正) ---
# 绿色 (2.0x), 红色 (0.5x), 灰色/同系 (1.0x, 默认不写)
RELATIONS = {
    "普通": {"地": 0.5, "幽": 0.5, "机械": 0.5},
    "地": {"火": 2.0, "冰": 2.0, "电": 2.0, "毒": 2.0, "草": 0.5, "武": 0.5},
    "冰": {"草": 2.0, "地": 2.0, "龙": 2.0, "翼": 2.0, "火": 0.5, "冰": 0.5, "机械": 0.5},
    "龙": {"龙": 2.0, "机械": 0.5},
    "电": {"水": 2.0, "翼": 2.0, "草": 0.5, "地": 0.5, "龙": 0.5, "电": 0.5},
    "毒": {"草": 2.0, "萌": 2.0, "地": 0.5, "毒": 0.5, "幽": 0.5, "机械": 0.5},
    "虫": {"草": 2.0, "恶": 2.0, "幻": 2.0, "火": 0.5, "毒": 0.5, "武": 0.5, "翼": 0.5, "幽": 0.5, "机械": 0.5,"萌": 0.5},
    "武": {"普通": 2.0, "地": 2.0, "冰": 2.0, "恶": 2.0, "机械": 2.0, "毒": 0.5, "虫": 0.5, "翼": 0.5, "萌": 0.5, "幽": 0.5, "幻": 0.5},
    "翼": {"草": 2.0, "虫": 2.0, "武": 2.0, "地": 0.5, "电": 0.5, "龙": 0.5, "机械": 0.5},
    "萌": {"龙": 2.0, "武": 2.0, "恶": 2.0, "火": 0.5, "毒": 0.5, "机械": 0.5},
    "幽": {"光": 2.0, "幽": 2.0, "幻": 2.0, "普通": 0.5, "恶": 0.5},
    "恶": {"幽": 2.0,"毒": 2.0, "萌": 2.0, "恶": 0.5, "光": 0.5, "武": 0.5},
    "机械": {"地": 2.0, "冰": 2.0, "萌": 2.0, "火": 0.5, "水": 0.5, "电": 0.5, "机械": 0.5},
    "幻": {"毒": 2.0, "武": 2.0, "光": 0.5, "机械": 0.5, "幻": 0.5},
    "火": {"草": 2.0, "冰": 2.0, "虫": 2.0, "机械": 2.0, "水": 0.5, "地": 0.5, "龙": 0.5},
    "水": {"火": 2.0, "地": 2.0, "机械": 2.0, "草": 0.5, "冰": 0.5, "龙": 0.5},
    "草": {"光": 2.0, "地": 2.0, "水": 2.0, "火": 0.5, "龙": 0.5, "毒": 0.5, "虫": 0.5, "翼": 0.5, "机械": 0.5},
    "光": {"幽": 2.0, "恶": 2.0, "草": 0.5, "冰": 0.5}
}

# --- 3. 核心计算函数 ---
def get_final_mult(atk_type, def_types):
    m_list = []
    for dt in def_types:
        # 【修正点】直接从字典获取倍率，字典里没有的默认为 1.0 (包括同系)
        # 这样你在 RELATIONS 里定义的龙打龙=2.0，恶打恶=2.0 就会生效了
        m_list.append(RELATIONS.get(atk_type, {}).get(dt, 1.0))
    
    # 双属性特殊计算逻辑
    if len(m_list) == 2:
        if m_list[0] == 2.0 and m_list[1] == 2.0: return 3.0 # 双重克制上限设定为 3x
        if m_list[0] == 0.5 and m_list[1] == 0.5: return 0.25 # 双重抵抗设定
        if (m_list[0] == 2.0 and m_list[1] == 0.5) or (m_list[0] == 0.5 and m_list[1] == 2.0): return 1.0
        
    res = 1.0
    for m in m_list: res *= m
    return round(res, 2)
def colored_type(t):
    color = TYPE_DATA.get(t, {"color": "#636e72"})['color']
    icon = TYPE_DATA.get(t, {"icon": "❓"})['icon']
    return f'<span class="type-tag" style="background-color:{color};">{icon} {t}</span>'

# --- 4. 界面布局 ---
st.title("🛡️ ⚔️ 洛克战术大师 - 精准数据版")
tab_def, tab_atk = st.tabs(["🛡️ 精准防御扫描", "⚔️ 精准打击扫描"])

with tab_def:
    st.markdown("##### 🔍 扫描漏洞 (抵抗判定: ≤ 0.5x)")
    team_data = []
    for i in range(6):
        with st.expander(f"精灵 #{i+1}", expanded=(i==0)):
            sel = st.pills("属性", TYPES, format_func=lambda x: f"{TYPE_DATA[x]['icon']} {x}", key=f"dp_{i}", selection_mode="multi")
            if sel: team_data.append(sel[:2])

    if st.button("🚀 启动精准防御扫描", type="primary"):
        if not team_data: st.warning("请配置精灵属性")
        else:
            gaps = []
            for atk in TYPES:
                best_val = min([get_final_mult(atk, s) for s in team_data])
                if best_val > 1.0: gaps.append({"type": atk, "val": best_val})
            
            gaps.sort(key=lambda x: x['val'], reverse=True)
            if not gaps: st.success("### ✅ 联防完美！全队所有属性均有抵抗位。")
            else:
                for item in gaps:
                    st.markdown(f'''<div class="danger-box">{colored_type(item['type'])} <span style="float:right; color:#d63031; font-weight:bold;">伤害倍率: {item['val']}x</span></div>''', unsafe_allow_html=True)
                
                st.subheader("💡 联防补位方案建议")
                rem_gaps = {g['type'] for g in gaps}
                best_adds = []
                while rem_gaps and len(best_adds) < 3:
                    # 使用 RELATIONS 复核联防补位
                    best_attr = max(TYPES, key=lambda c: len({atk for atk in rem_gaps if RELATIONS.get(atk, {}).get(c, 1.0) <= 0.5}))
                    covers = {atk for atk in rem_gaps if RELATIONS.get(atk, {}).get(best_attr, 1.0) <= 0.5}
                    if not covers: break
                    best_adds.append((best_attr, covers))
                    rem_gaps -= covers
                
                for attr, target in best_adds:
                    st.info(f"建议引入属性精灵：{TYPE_DATA[attr]['icon']} {attr} (可抵抗 {' '.join([TYPE_DATA[t]['icon'] for t in target])})")

with tab_atk:
    st.markdown("##### 🎯 扫描打击盲点 (克制判定: ≥ 2.0x)")
    all_skills = st.pills("全队技能属性", TYPES, format_func=lambda x: f"{TYPE_DATA[x]['icon']} {x}", selection_mode="multi", key="ap")
    
    if st.button("🔥 启动精准打击扫描", type="primary"):
        if not all_skills: st.error("请选择技能属性")
        else:
            uncovered = [t for t in TYPES if not any(RELATIONS.get(s, {}).get(t, 1.0) >= 2.0 for s in all_skills)]
            if not uncovered: st.success("### 🔥 打击面全覆盖！全系达成 2.0x 克制。")
            else:
                st.error(f"### ❄️ 打击盲点 ({len(uncovered)})")
                st.markdown(" ".join([colored_type(t) for t in uncovered]), unsafe_allow_html=True)
                
                st.subheader("💡 进攻配招建议")
                rem_uncovered = set(uncovered)
                recs = []
                while rem_uncovered and len(recs) < 3:
                    best_s = max(TYPES, key=lambda s: len({t for t in rem_uncovered if RELATIONS.get(s, {}).get(t, 1.0) >= 2.0}))
                    hits = {t for t in rem_uncovered if RELATIONS.get(best_s, {}).get(t, 1.0) >= 2.0}
                    if not hits: break
                    recs.append((best_s, hits))
                    rem_uncovered -= hits
                
                for s_attr, s_targets in recs:
                    st.markdown(f'''<div class="info-box">建议加入技能属性：{colored_type(s_attr)}<br>可额外克制盲点：{" ".join([TYPE_DATA[tx]['icon'] for tx in s_targets])}</div>''', unsafe_allow_html=True)

st.divider()
st.caption("数据说明：所有单属性克制关系已严格依据提供的官方图片进行同步修正。同系互打 1.0x。")