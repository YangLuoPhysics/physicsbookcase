import streamlit as st
from streamlit_option_menu import option_menu

# --- 1. 頂端設定區 ---
st.set_page_config(page_title="物理漫遊天地 | 羊珞老師", page_icon="🐑", layout="wide")

# 虛擬用戶名單 (帳號設定處)
USER_DB = {
    "admin": {"pw": "yangluo888", "name": "羊珞老師", "role": "老師"},
    "S001": {"pw": "physics123", "name": "林同學", "role": "學生", "progress": 85},
    "S002": {"pw": "physics123", "name": "王同學", "role": "學生", "progress": 40},
}

# 初始化身分狀態
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "訪客"
    st.session_state['user_name'] = "遊客"

# --- 2. 側邊欄邏輯區 (身分驗證) ---
with st.sidebar:
    st.title("🐑 羊珞老師的實驗室")
    st.write("「物理不只是公式，是理解世界的自由。」")
    st.markdown("---")
    
    if st.session_state['user_role'] == "訪客":
        st.subheader("🔑 系統登入")
        input_user = st.text_input("學號 / 帳號")
        input_password = st.text_input("通行密碼", type="password")
        if st.button("驗證身分"):
            if input_user in USER_DB and USER_DB[input_user]["pw"] == input_password:
                st.session_state['user_role'] = USER_DB[input_user]["role"]
                st.session_state['user_name'] = USER_DB[input_user]["name"]
                st.session_state['current_uid'] = input_user
                st.success(f"歡迎，{st.session_state['user_name']}！")
                st.rerun()
            else:
                st.error("驗證失敗，請檢查帳密。")
    else:
        st.write(f"當前身分：**{st.session_state['user_role']}**")
        st.write(f"使用者：{st.session_state['user_name']}")
        if st.button("登出系統"):
            st.session_state['user_role'] = "訪客"
            st.session_state['user_name'] = "遊客"
            st.rerun()

# --- 3. 動態導覽選單 ---
# 根據身分定義選單選項
if st.session_state['user_role'] == "老師":
    menu_options = ["物奧講堂", "模擬實驗室", "思維試煉(作業)", "導師批改室", "萬有引力園地"]
    menu_icons = ["book", "cpu", "pencil-fill", "check2-circle", "chat-dots"]
elif st.session_state['user_role'] == "學生":
    menu_options = ["物奧講堂", "模擬實驗室", "我的學習進度", "思維試煉(作業)", "萬有引力園地"]
    menu_icons = ["book", "cpu", "graph-up-arrow", "pencil-fill", "chat-dots"]
else: # 訪客
    menu_options = ["物奧講堂", "模擬實驗室"]
    menu_icons = ["book", "cpu"]

selected = option_menu(
    menu_title=None, 
    options=menu_options, 
    icons=menu_icons, 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal"
)

# --- 4. 主畫面分頁區 ---

# A. 物奧講堂
if selected == "物奧講堂":
    st.header("🧬 物奧專題講義")
    st.write("這裡是公開的物理知識庫，歡迎漫遊。")
    col1, col2 = st.columns(2)
    with col1:
        st.info("講義 01：變質量系統")
        st.markdown("[📥 點我預覽講義連結](https://example.com)")
    with col2:
        st.info("講義 02：剛體轉動")
        st.markdown("[📥 點我預覽講義連結](https://example.com)")

# B. 模擬實驗室
elif selected == "模擬實驗室":
    st.header("🔬 怪奇物理實驗室")
    st.components.v1.iframe("https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html", height=600)

# C. 我的學習進度 (僅學生可見)
elif selected == "我的學習進度":
    st.header(f"📊 {st.session_state['user_name']} 的學習軌跡")
    uid = st.session_state['current_uid']
    progress_val = USER_DB[uid]["progress"]
    st.write(f"本學期物理特訓達成率：{progress_val}%")
    st.progress(progress_val / 100)
    st.write("💡 完成更多作業來提升你的進度條吧！")

# D. 思維試煉(作業) (學生與老師可見)
elif selected == "思維試煉(作業)":
    st.header("✍️ 課後邏輯試煉")
    st.write("請跳轉至 Google Classroom 進行作業繳交。")
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("🏫 進入 Google Classroom", "https://classroom.google.com", icon="🚀")
    with c2:
        st.link_button("📝 檢視本週特定作業", "https://classroom.google.com", icon="📤")

# E. 導師批改室 (僅老師可見)
elif selected == "導師批改室":
    st.header("🖋️ 羊珞老師的批改桌")
    st.write("目前班級繳交概況：")
    st.table({
        "學號": ["S001", "S002"],
        "姓名": ["林同學", "王同學"],
        "進度": ["85%", "40%"],
        "狀態": ["待批改", "未繳交"]
    })
    st.button("開啟線上繪圖批改工具 (開發中)")

# F. 萬有引力園地
elif selected == "萬有引力園地":
    st.header("💬 萬有引力討論園地")
    st.text_area("有什麼物理難題想跟大家討論嗎？")
    if st.button("送出訊息"):
        st.success("訊息已發布！")

# --- 5. 頁尾 ---
st.markdown("---")
st.caption(f"© 2026 物理漫遊天地 - 當前身分：{st.session_state['user_role']} | 咩～🐑")
