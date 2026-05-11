import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components # 新增這一行

# --- 1. 頂端設定區 ---
st.set_page_config(page_title="物理漫遊天地 | 羊珞老師", page_icon="🐑", layout="wide")

# 虛擬用戶數據庫 (帳號、密碼、姓名、角色、進度)
USER_DB = {
    "admin": {"pw": "yangluo888", "name": "羊珞老師", "role": "老師"},
    "S001": {"pw": "physics123", "name": "林同學", "role": "學生", "progress": 85},
    "S002": {"pw": "physics123", "name": "王同學", "role": "學生", "progress": 40},
}

# 初始化身分狀態 (預設為訪客)
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "遊客"
    st.session_state['user_name'] = "一般遊客"

# --- 2. 側邊欄：身分驗證與羊珞小羊動畫 ---
with st.sidebar:
    st.title("🐑 物理漫遊天地")
    
    # 【SVG 動畫位置】: 這裡可以放置您的 SVG 代碼
    svg_mascot = """
    <svg width="200" height="150" viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
      <circle cx="100" cy="75" r="40" fill="#f8f9fa" stroke="#005088" stroke-width="2">
        <animate attributeName="cy" values="75;65;75" dur="2s" repeatCount="indefinite" />
      </circle>
      <text x="75" y="80" font-family="Arial" font-size="12" fill="#005088">咩~ Science</text>
    </svg>
    """
    st.markdown(svg_mascot, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 登入邏輯
    if st.session_state['user_role'] == "遊客":
        st.subheader("🔑 成員登入")
        u = st.text_input("帳號/學號")
        p = st.text_input("密碼", type="password")
        if st.button("驗證進入"):
            if u in USER_DB and USER_DB[u]["pw"] == p:
                st.session_state['user_role'] = USER_DB[u]["role"]
                st.session_state['user_name'] = USER_DB[u]["name"]
                st.session_state['current_uid'] = u
                st.rerun()
            else:
                st.error("邏輯驗證失敗")
    else:
        st.write(f"當前身分：**{st.session_state['user_role']}**")
        st.write(f"歡迎，{st.session_state['user_name']}")
        if st.button("登出"):
            st.session_state['user_role'] = "遊客"
            st.rerun()

# --- 3. 動態導覽選單架構 ---
if st.session_state['user_role'] == "老師":
    menu = ["物理新知", "PhET實驗室", "Google Classroom", "教師後台"]
    icons = ["lightbulb", "cpu", "send", "shield-lock"]
elif st.session_state['user_role'] == "學生":
    menu = ["物理新知", "PhET實驗室", "我的進度", "Google Classroom"]
    icons = ["lightbulb", "cpu", "graph-up", "send"]
else: # 遊客
    menu = ["物理新知", "PhET實驗室"]
    icons = ["lightbulb", "cpu"]

selected = option_menu(None, options=menu, icons=icons, orientation="horizontal")

# --- 4. 主畫面分頁內容區 ---

# 【遊客與全員區】：物理新知
if selected == "物理新知":
    st.header("✨ 物理漫遊：今日新知")
    st.write("在這裡，我們用最簡單的語言，解構宇宙的奧祕。")
    st.info("💡 建築中的物理：為何摩天大樓在強風中不會倒下？ (受力分析專題)")

# 【遊客與全員區】：PhET 實驗室
elif selected == "PhET實驗室":
    st.header("🔬 互動模擬實驗室")
    # 這裡可以切換不同的模擬器
    st.components.v1.iframe("https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html", height=600)

# 【學生專屬】：進度追蹤
elif selected == "我的進度":
    uid = st.session_state['current_uid']
    st.header(f"📊 {st.session_state['user_name']} 的學習軌跡")
    prog = USER_DB[uid]["progress"]
    st.progress(prog / 100)
    st.write(f"目前課程完成率：{prog}%")

# 【學生/老師】：Google Classroom 連動
elif selected == "Google Classroom":
    st.header("🏫 教學雲端聯結")
    st.write("講義傳承、作業派發與線上討論。")
    st.link_button("🚀 前往 Classroom 繳交作業", "https://classroom.google.com")

# 【教師專屬】：後台觀察室
elif selected == "教師後台":
    st.header("👁️ 羊珞老師的戰略觀測站")
    st.write("這裡可以觀察所有學生的「玄機」與進度。")
    st.table(USER_DB) # 快速觀察名單數據
