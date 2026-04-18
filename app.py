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
    st.write("「物理不只是公式，是理解世界的自由。」")
    
    # 簡易身分選擇 (實際應用時應透過帳密登入)
    role = st.selectbox("請選擇你的登入身分：", ["訪客", "學生", "羊珞老師 (Admin)"])
    if st.button("確認進入"):
        st.session_state['user_role'] = role
        st.success(f"目前以 {role} 身分漫遊中")

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
        if st.session_state['user_role'] in ["學生", "羊珞老師 (Admin)"]:
            st.warning("本週題目：分析『羊珞建築』的靜力平衡。")
            uploaded_file = st.file_uploader("請上傳你的解題照片或 PDF (限定 200MB 內)", type=['png', 'jpg', 'pdf'])
            if uploaded_file is not None:
                st.success("檔案上傳成功！羊珞老師會盡快批改，咩～")
        else:
            st.error("請先登入學生身分以存取作業區。")

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
