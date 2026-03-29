import streamlit as st

# --- 1. 页面配置 ---
st.set_page_config(page_title="洛克王国战术分析器", page_icon="🛡️", layout="wide")

# --- 2. 基础数据定义 ---
TYPES = ["无", "普通", "草", "火", "水", "光", "地", "冰", "龙", "电", "毒", "虫", "武", "翼", "萌", "幽", "恶", "机械", "幻"]

# 原始克制数据 (基于图片提取)
# 格式: {攻击系: {防御系: 倍率}}
RAW_RELATIONS = {
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

# 辅助函数：计算单次攻击倍率
def get_multiplier(atk_type, def_type):
    if atk_type == "无" or def_type == "无": return 1.0
    return RAW_RELATIONS.get(atk_type, {}).get(def_type, 1.0)

# --- 3. 侧边栏导航 ---
st.sidebar.title("💎 功能选择")
mode = st.sidebar.radio("请选择分析模式：", ["🛡️ 防御盲点分析", "⚔️ 打击面分析"])

# --- 4. 功能逻辑 ---

if mode == "🛡️ 防御盲点分析":
    st.title("🛡️ 全队防御盲点分析")
    st.write("输入精灵属性，寻找全队都**接不住**（均被克制）的属性攻击。")
    
    team_sprites = []
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            st.markdown(f"**精灵 {i+1}**")
            a1 = st.selectbox(f"主属性", TYPES[1:], key=f"def_a1_{i}")
            a2 = st.selectbox(f"副属性", TYPES, key=f"def_a2_{i}")
            team_sprites.append([a1, a2] if a2 != "无" else [a1])

    if st.button("开始深度扫描防御漏洞", use_container_width=True):
        st.divider()
        gaps = []
        for atk in TYPES[1:]:
            # 计算全队面对该攻击时的表现
            team_results = []
            for sprite in team_sprites:
                mult = 1.0
                for attr in sprite:
                    mult *= get_multiplier(atk, attr)
                team_results.append(mult)
            
            # 全队最好的防守位点
            best_defense = min(team_results)
            if best_defense >= 2.0:
                gaps.append((atk, best_defense))

        if gaps:
            st.error("### ⚠️ 警报：发现全队通用弱点")
            for g, val in gaps:
                st.warning(f"**{g}系**：全队无人能抗，最小伤害高达 **{val}x**")
        else:
            st.success("### ✅ 联防稳固：全队对所有属性均有应对方案。")

else:
    st.title("⚔️ 打击面分析")
    st.write("输入全队拥有的**攻击技能属性**，查看是否存在克制盲区。")
    
    skill_pool = []
    cols = st.columns(3)
    for i in range(6):
        with cols[i % 3]:
            skills = st.multiselect(f"精灵 {i+1} 技能属性", TYPES[1:], key=f"atk_s_{i}")
            skill_pool.extend(skills)
    
    final_skills = list(set(skill_pool))

    if st.button("开始分析打击覆盖率", use_container_width=True):
        st.divider()
        if not final_skills:
            st.error("请至少选择一个技能属性！")
        else:
            covered = []
            uncovered = []
            for target in TYPES[1:]:
                # 只要有一个技能能打出2倍伤害，就算覆盖
                if any(get_multiplier(s, target) >= 2.0 for s in final_skills):
                    covered.append(target)
                else:
                    uncovered.append(target)
            
            c1, c2 = st.columns(2)
            with c1:
                st.success(f"🔥 已覆盖 ({len(covered)}):")
                st.caption("面对这些属性的敌人，你拥有克制手段。")
                st.write(" 、".join(covered))
            with c2:
                st.error(f"❄️ 未覆盖 ({len(uncovered)}):")
                st.caption("面对这些属性，你全队最高只能打出 1.0x 伤害。")
                st.write(" 、".join(uncovered) if uncovered else "全属性克制已达成！")

# --- 5. 页脚 ---
st.sidebar.markdown("---")
st.sidebar.caption("洛克王国属性分析工具 v2.0")