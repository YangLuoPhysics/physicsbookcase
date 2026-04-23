import streamlit as st
from streamlit_option_menu import option_menu

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="物理漫遊天地 | 羊珞老師", page_icon="🐑", layout="wide")

# --- 2. 模擬登入系統 (V1 簡化版) ---
# 提示：未來將接上 Firebase Authentication
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = None

with st.sidebar:
    st.title("🐑 羊珞老師的實驗室")
    
    # 取代原本的 Selectbox
    input_user = st.text_input("學號 (Username)")
    input_password = st.text_input("通行密碼 (Password)", type="password")
    
    if st.button("驗證身分"):
        # 簡單的邏輯判斷 (未來可換成 Secrets 或資料庫)
        if input_user == "admin" and input_password == "yangluo888":
            st.session_state['user_role'] = "羊珞老師 (Admin)"
            st.success("老師好！系統已解鎖。")
        elif input_user.startswith("S") and input_password == "physics123":
            st.session_state['user_role'] = "學生"
            st.success("驗證成功，歡迎進入漫遊天地！")
        else:
            st.error("邏輯驗證失敗，請檢查帳密。")

# --- 3. 主導覽選單 ---
if st.session_state['user_role']:
    selected = option_menu(
        menu_title=None,
        options=["物奧講堂", "思維試煉(作業)", "模擬實驗室", "萬有引力園地", "導師批改室"],
        icons=["book", "pencil-fill", "cpu", "chat-dots", "check2-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # --- 4. 各區塊內容 ---
    
    # A. 物奧講堂 (講義派發)
    if selected == "物奧講堂":
        st.header("🧬 物奧專題講義")
        st.write("這裡存放著羊珞老師精心編寫的物奧特訓資源。")
        col1, col2 = st.columns(2)
        with col1:
            st.info("講義 01：變質量系統與火箭方程")
            st.button("下載 PDF 講義", key="dl1")
        with col2:
            st.info("講義 02：剛體轉動與慣性張量初探")
            st.button("下載 PDF 講義", key="dl2")

    # B. 思維試煉 (學生作業提交) 
    elif selected == "思維試煉(作業)":
        st.header("✍️ 課後邏輯試煉")
        
        # 建立兩個分欄，讓畫面更整齊
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📌 本週進度：剛體轉動與角動量")
            st.write("請先閱讀講義後，完成 GC 上的三題挑戰題。")
            # 跳轉到 Google Classroom 課程主頁
            st.link_button("🏫 進入 Google Classroom", "https://classroom.google.com/w/NzAxMjAwNzAyNjE4/t/all")
            
        with col2:
            st.warning("⏰ 繳交期限：週五 23:59")
            st.write("如果對題目有疑問，可以先到『萬有引力園地』提問喔！")
            # 跳轉到特定的一份作業頁面
            st.link_button("📝 點我直接繳交作業", "請在此貼上特定作業的網址")

    # C. 模擬實驗室 (模擬器整合)
    elif selected == "模擬實驗室":
        st.header("🔬 怪奇物理實驗室")
        st.write("透過調整參數，觀察現象的變遷。")
        # 嵌入 PhET 或 GeoGebra (範例：拋體運動)
        st.components.v1.iframe("https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html", height=600)

    # D. 萬有引力園地 (討論區)
    elif selected == "萬有引力園地":
        st.header("💬 萬有引力討論園地")
        st.text_area("輸入你的想法或問題...", placeholder="例如：老師，角動量守恆在非慣性系要怎麼修正？")
        if st.button("發布討論"):
            st.balloons()
            st.success("你的訊息已漂浮在知識的海洋中。")

    # E. 導師批改室 (權限管理)
    elif selected == "導師批改室":
        st.header("🖋️ 羊珞老師的批改桌")
        if st.session_state['user_role'] == "羊珞老師 (Admin)":
            st.write("目前待批改清單：")
            st.table({
                "學生姓名": ["林同學", "王同學", "張同學"],
                "繳交時間": ["10:20 AM", "11:15 AM", "12:00 PM"],
                "狀態": ["待批改", "待批改", "已完成"]
            })
            # 這裡未來會放入 Canvas 批改功能
            st.button("開啟線上繪圖批改工具")
        else:
            st.error("此區域僅限『羊珞老師』權限進入，請遵守實驗室規範！")

else:
    st.info("請從左側選單選擇身分進入『物理漫遊天地』。")

# --- 5. 頁尾 ---
st.markdown("---")
st.caption("© 2026 物理漫遊天地 - 羊珞老師版權所有 | 邏輯與溫柔的結晶")
