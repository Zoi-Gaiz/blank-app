import streamlit as st

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="洛克战术大师", 
    page_icon="🛡️", 
    layout="centered" # 手机端居中对齐更美观
)

# 注入 CSS 增强移动端按钮点击感
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        border-radius: 10px;
        font-weight: bold;
    }
    div[data-testid="stExpander"] {
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 核心克制数据 (18x18) ---
TYPES = ["普通", "草", "火", "水", "光", "地", "冰", "龙", "电", "毒", "虫", "武", "翼", "萌", "幽", "恶", "机械", "幻"]

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

# --- 3. UI 主逻辑 ---
st.title("🛡️ 洛克战术大师")
st.caption("移动端点选优化版 | 2026 赛季数据")

tab_def, tab_atk = st.tabs(["🛡️ 防御扫描", "⚔️ 打击覆盖"])

# --- 防御模式 ---
with tab_def:
    st.markdown("##### 🔍 扫描全队共同天敌")
    team_data = []
    for i in range(6):
        with st.expander(f"精灵 #{i+1} 属性配置", expanded=(i == 0)):
            # st.pills 是手机端最高效的选择方式
            selected = st.pills(
                "点击属性图标 (限2个)", 
                TYPES, 
                key=f"def_pills_{i}", 
                selection_mode="multi"
            )
            if len(selected) > 2:
                st.toast("⚠️ 一只精灵最多2个属性", icon="🚨")
                selected = selected[:2]
            team_data.append(selected if selected else ["普通"])

    if st.button("🚀 启动扫描", type="primary"):
        gaps = []
        for enemy_atk in TYPES:
            # 找到全队对该属性承伤的最小值
            all_sprite_dmg = []
            for sprite in team_data:
                mult = 1.0
                for attr in sprite:
                    mult *= get_mult(enemy_atk, attr)
                all_sprite_dmg.append(mult)
            
            best_def = min(all_sprite_dmg)
            if best_defense >= 2.0:
                gaps.append((enemy_atk, best_def))

        if gaps:
            st.error("### ❌ 致命：全队均会被以下属性穿透")
            for g, v in gaps:
                st.warning(f"**{g}系攻击**：全队无人能抗 (受损 ≥{v}x)")
        else:
            st.success("### ✅ 联防完美！没有任何属性可以一穿六。")

# --- 打击模式 ---
with tab_atk:
    st.markdown("##### 🎯 扫描全队打击盲区")
    # 手机端平铺所有属性，直接点选
    all_skills = st.pills(
        "点击选择全队已学习的所有技能属性 (多选)", 
        TYPES, 
        selection_mode="multi",
        key="atk_pills_main"
    )

    if st.button("🔥 分析覆盖率", type="primary"):
        if not all_skills:
            st.error("请先点击上方按钮选择技能属性！")
        else:
            uncovered = []
            for target in TYPES:
                if not any(get_mult(s, target) >= 2.0 for s in all_skills):
                    uncovered.append(target)
            
            if uncovered:
                st.error(f"### ❄️ 打击盲点 ({len(uncovered)})")
                st.info("当对手是以下属性时，你没有任何技能可以造成2倍克制：")
                st.write(" 、".join(uncovered))
            else:
                st.success("### 🔥 完美打击面！全属性克制已达成。")

# --- 页脚 ---
st.divider()
st.caption("Tip: 在手机浏览器菜单中选择“添加到主屏幕”可作为 App 使用。")