import streamlit as st
from utils import TYPE_DATA, TYPES, RELATIONS, get_final_mult

# --- 1. 样式与配置 ---
st.set_page_config(page_title="洛克战术大师 Pro", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    .type-tag { padding: 4px 10px; border-radius: 6px; color: white; font-weight: bold; margin-right: 8px; display: inline-block; }
    .status-card { border-radius: 10px; padding: 12px; margin-bottom: 10px; border-left: 5px solid; }
    .perfect { background-color: #f0fff4; border-color: #2ecc71; }
    .half-perfect { background-color: #fffaf0; border-color: #f1c40f; }
    .danger { background-color: #fff5f5; border-color: #d63031; }
    .stButton > button { border-radius: 8px; height: 3rem; font-weight: bold; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

# 初始化状态
if 'team_pets' not in st.session_state:
    st.session_state.team_pets = [[] for _ in range(6)]

def colored_type(t):
    data = TYPE_DATA.get(t, {"color": "#636e72", "icon": "❓"})
    return f'<span class="type-tag" style="background-color:{data["color"]};">{data["icon"]} {t}</span>'

# --- 2. 侧边栏：打击面配置 ---
with st.sidebar:
    st.header("⚔️ 全队技能池")
    # 使用 multiselect 保证状态在点击九宫格时不丢失
    selected_skills = st.multiselect(
        "配置技能属性", TYPES, 
        format_func=lambda x: f"{TYPE_DATA[x]['icon']} {x}",
        key="skill_pool"
    )
    if st.button("🧹 清空所有选择"):
        st.session_state.team_pets = [[] for _ in range(6)]
        st.rerun()

# --- 3. 主界面：九宫格防御选择 ---
st.title("🛡️ ⚔️ 洛克战术大师：攻防一体扫描")
st.subheader("🛡️ 队伍属性配置 (每宠点击 1-2 个属性)")

pet_tabs = st.tabs([f"精灵 #{i+1}" for i in range(6)])

for i in range(6):
    with pet_tabs[i]:
        # 3行6列的整齐九宫格
        for row in range(3):
            cols = st.columns(6)
            for col_idx in range(6):
                idx = row * 6 + col_idx
                if idx < len(TYPES):
                    t = TYPES[idx]
                    is_sel = t in st.session_state.team_pets[i]
                    
                    # 点击按钮逻辑
                    if cols[col_idx].button(
                        f"{TYPE_DATA[t]['icon']} {t}", 
                        key=f"p{i}_{t}", 
                        type="primary" if is_sel else "secondary",
                        use_container_width=True
                    ):
                        if is_sel:
                            st.session_state.team_pets[i].remove(t)
                        elif len(st.session_state.team_pets[i]) < 2:
                            st.session_state.team_pets[i].append(t)
                        st.rerun()

st.divider()

# --- 4. 自动化分析与建议 ---
active_pets = [p for p in st.session_state.team_pets if p]

if not active_pets or not selected_skills:
    st.info("💡 请在上方九宫格选择**精灵属性**，并在侧边栏选择**技能属性**。")
else:
    # 执行扫描
    scan_res = []
    for opponent in TYPES:
        best_def = min([get_final_mult(opponent, p) for p in active_pets])
        can_crack = any([RELATIONS.get(s, {}).get(opponent, 1.0) >= 2.0 for s in selected_skills])
        scan_res.append({"target": opponent, "def": best_def, "crack": can_crack})

    # 结果看板
    def_gaps = [r for r in scan_res if r['def'] > 0.5]
    atk_gaps = [r for r in scan_res if not r['crack']]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("完美覆盖", f"{18 - max(len(def_gaps), len(atk_gaps))}/18")
    c2.metric("防御漏洞", f"{len(def_gaps)}个")
    c3.metric("打击盲点", f"{len(atk_gaps)}个")

    # 弱点卡片展示
    st.subheader("⚠️ 弱点监控")
    weak_items = [r for r in scan_res if r['def'] > 0.5 or not r['crack']]
    
    if not weak_items:
        st.success("🎉 完美！攻防两端均无死角。")
    else:
        grid = st.columns(4)
        for idx, r in enumerate(weak_items):
            with grid[idx % 4]:
                is_danger = r['def'] > 1.0 and not r['crack']
                sc = "danger" if is_danger else "half-perfect"
                st.markdown(f"""
                    <div class="status-card {sc}">
                        <strong>{colored_type(r['target'])}</strong><br>
                        <small>防: {"✅" if r['def']<=0.5 else f"❌({r['def']}x)"} | 攻: {"✅" if r['crack'] else "❌"}</small>
                    </div>
                """, unsafe_allow_html=True)

    # --- 5. 补位建议算法 ---
    st.subheader("💡 专家补位建议")
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.write("**🛡️ 防守补位 (寻求0.5x):**")
        rem_def = {r['target'] for r in def_gaps}
        for _ in range(2):
            if not rem_def: break
            best = max(TYPES, key=lambda c: len({atk for atk in rem_def if RELATIONS.get(atk, {}).get(c, 1.0) <= 0.5}))
            covered = {atk for atk in rem_def if RELATIONS.get(atk, {}).get(best, 1.0) <= 0.5}
            if not covered: break
            st.markdown(f"建议加入 {colored_type(best)} 抵抗 {' '.join([TYPE_DATA[x]['icon'] for x in covered])}", unsafe_allow_html=True)
            rem_def -= covered

    with col_r:
        st.write("**⚔️ 攻击补位 (寻求2.0x):**")
        rem_atk = {r['target'] for r in atk_gaps}
        for _ in range(2):
            if not rem_atk: break
            best = max(TYPES, key=lambda s: len({t for t in rem_atk if RELATIONS.get(s, {}).get(t, 1.0) >= 2.0}))
            covered = {t for t in rem_atk if RELATIONS.get(best, {}).get(t, 1.0) >= 2.0}
            if not covered: break
            st.markdown(f"建议技能 {colored_type(best)} 克制 {' '.join([TYPE_DATA[x]['icon'] for x in covered])}", unsafe_allow_html=True)
            rem_atk -= covered