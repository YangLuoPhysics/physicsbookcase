import streamlit as st
from streamlit_option_menu import option_menu

# ==========================================
# 1. 系統配置區
# ==========================================
st.set_page_config(page_title="物理漫遊天地 | 羊珞老師", page_icon="🐑", layout="wide")

# 虛擬用戶數據庫
USER_DB = {
    "admin": {"pw": "yangluo888", "name": "羊珞老師", "role": "老師"},
    "S001": {"pw": "physics123", "name": "林同學", "role": "學生", "progress": 85},
    "S002": {"pw": "physics123", "name": "王同學", "role": "學生", "progress": 40},
}

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "遊客"
    st.session_state['user_name'] = "一般遊客"

# ==========================================
# 2. 側邊欄 (登入與導引)
# ==========================================
with st.sidebar:
    st.title("🐑 物理漫遊天地")
    st.write("「連結 AI 邏輯，漫遊物理世界。」")
    st.markdown("---")
    
    if st.session_state['user_role'] == "遊客":
        st.subheader("🔑 成員登入")
        u = st.text_input("學號 / 帳號")
        p = st.text_input("通行密碼", type="password")
        if st.button("驗證進入"):
            if u in USER_DB and USER_DB[u]["pw"] == p:
                st.session_state['user_role'] = USER_DB[u]["role"]
                st.session_state['user_name'] = USER_DB[u]["name"]
                st.session_state['current_uid'] = u
                st.rerun()
            else:
                st.error("驗證失敗")
    else:
        st.write(f"當前身分：**{st.session_state['user_role']}**")
        st.write(f"歡迎回來，{st.session_state['user_name']}")
        if st.button("登出系統"):
            st.session_state['user_role'] = "遊客"
            st.rerun()

# ==========================================
# 3. 主導覽選單
# ==========================================
if st.session_state['user_role'] == "老師":
    menu = ["物理新知", "PhET實驗室", "Google Classroom", "教師後台"]
    icons = ["lightbulb", "cpu", "send", "shield-lock"]
elif st.session_state['user_role'] == "學生":
    menu = ["物理新知", "PhET實驗室", "我的進度", "Google Classroom"]
    icons = ["lightbulb", "cpu", "graph-up", "send"]
else:
    menu = ["物理新知", "PhET實驗室"]
    icons = ["lightbulb", "cpu"]

selected = option_menu(None, options=menu, icons=icons, orientation="horizontal")

# ==========================================
# 4. 分頁內容執行
# ==========================================

# --- A. 物理新知 (專題連結庫) ---
if selected == "物理新知":
    st.header("✨ 物理漫遊：專題導覽")
    st.write("老師與 AI 夥伴 Gemini 協作產出的邏輯筆記，點選下方專題開啟漫遊。")

    # 💡 老師看這裡！未來要增加新專題，只要在這裡增加一行即可
    TOPICS = {
        "🏙️ 建築中的物理：摩天大樓為何不倒？": {
            "url": "https://gemini.google.com/share/fec9b6478ac6",
            "desc": "深入探究受力分析、共振現象與調諧質量阻尼器 (TMD) 的減震魔法。"
        },
        "🪐 克卜勒與力學能守恆：行星軌道模擬器": {
            "url": "https://gemini.google.com/share/1147cbe3ad0e",
            "desc": "從橢圓軌道看見萬有引力與動能、位能的完美交織，理解行星運動的規律。"
        },
        "🌌 重力位能一般式：穿越星際的能量場": {
            "url": "https://gemini.google.com/share/c980bc66efa6",
            "desc": "從無窮遠處到近地表，探索萬有引力如何決定物體的勢能，並觀察能量在不同距離間的變化。"
        }
        # "🔭 你的下一個新知": {"url": "網址", "desc": "簡介"}
    }

    # 顯示下拉選單 (策略一)
    topic_name = st.selectbox("請選擇您想探索的專題：", list(TOPICS.keys()))
    
    # 顯示所選專題的卡片
    current_topic = TOPICS[topic_name]
    st.markdown("---")
    with st.container():
        st.subheader(topic_name)
        st.write(current_topic["desc"])
        st.link_button("🚀 前往該專題 (開啟 Gemini 邏輯筆記)", current_topic["url"], use_container_width=True)
        st.info("💡 提示：點擊按鈕後會開啟新視窗，您可以在那裡看到完整的物理推導過程。")

# --- B. PhET 實驗室 ---
elif selected == "PhET實驗室":
    st.header("🔬 官方互動模擬器")
    st.write("直接在網頁中操作物理量，觀察現象的變化。")
    st.components.v1.iframe("https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html", height=600)

# --- C. 我的進度 ---
elif selected == "我的進度":
    uid = st.session_state['current_uid']
    st.header(f"📊 {st.session_state['user_name']} 的學習軌跡")
    prog = USER_DB[uid]["progress"]
    st.progress(prog / 100)
    st.write(f"目前課程完成率：{prog}%")

# --- D. Google Classroom ---
elif selected == "Google Classroom":
    st.header("🏫 教學連動系統")
    st.link_button("🚀 前往 Classroom 繳交作業", "https://classroom.google.com")

# --- E. 教師後台 ---
elif selected == "教師後台":
    st.header("👁️ 戰略後台")
    st.table(USER_DB)

st.markdown("---")
st.caption("© 2026 物理漫遊天地 - 羊珞老師與 AI 協作開發 | 咩～🐑")
