import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components # 新增這一行

def render_skyscraper_sim():
    """
    將 React 摩天大樓模擬器封裝為 Streamlit 組件
    """
    skyscraper_html = """
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <div id="root"></div>

    <script type="text/babel">
      const { useState, useEffect, useRef } = React;

      function SkyscraperSim() {
        // --- 此處包含老師原始的物理邏輯 (已優化為可在 HTML 運行版本) ---
        const [windSpeed, setWindSpeed] = useState(5);
        const [tmdActive, setTmdActive] = useState(true);
        const [isPlaying, setIsPlaying] = useState(true);
        
        const H = 300; const W = 80; const M = 100; const K = 2.0; const C = 0.15;
        const m = 5; const k_tmd = 0.1; const c_tmd = 0.2;
        const naturalFreq = Math.sqrt(K / M);
        const maxHistory = 200;

        const physicsRef = useRef({
          time: 0, X: 0, vX: 0, y: 0, vy: 0,
          historyX: [], historyY: [], lastFrameTime: performance.now()
        });

        const [uiState, setUiState] = useState({ X: 0, y: 0, windForce: 0, tmdForce: 0, historyX: [], historyY: [] });

        const updatePhysics = (timestamp) => {
          if (!isPlaying) {
            physicsRef.current.lastFrameTime = timestamp;
            requestAnimationFrame(updatePhysics);
            return;
          }
          const dt = Math.min((timestamp - physicsRef.current.lastFrameTime) * 0.001, 0.05) * 5;
          physicsRef.current.lastFrameTime = timestamp;
          let { time, X, vX, y, vy, historyX, historyY } = physicsRef.current;
          time += dt;
          const windGustFreq = naturalFreq * 0.95;
          const currentWindForce = windSpeed * 0.5 + windSpeed * 1.2 * Math.sin(time * windGustFreq);
          let force_tmd_on_building = 0;
          if (tmdActive) {
            force_tmd_on_building = k_tmd * y + c_tmd * vy;
            const a_X_temp = (currentWindForce + force_tmd_on_building - K * X - C * vX) / M;
            const a_y = (-k_tmd * y - c_tmd * vy) / m - a_X_temp;
            vy += a_y * dt; y += vy * dt;
          } else {
            y *= 0.9; vy = 0;
          }
          const a_X = (currentWindForce + force_tmd_on_building - K * X - C * vX) / M;
          vX += a_X * dt; X += vX * dt;
          if (Math.random() < 0.5) {
            historyX.push(X); historyY.push(y);
            if (historyX.length > maxHistory) { historyX.shift(); historyY.shift(); }
          }
          physicsRef.current = { time, X, vX, y, vy, historyX, historyY, lastFrameTime: timestamp };
          setUiState({ X, y, windForce: currentWindForce, tmdForce: force_tmd_on_building, historyX: [...historyX], historyY: [...historyY] });
          requestAnimationFrame(updatePhysics);
        };

        useEffect(() => {
          const req = requestAnimationFrame(updatePhysics);
          return () => cancelAnimationFrame(req);
        }, [isPlaying, tmdActive, windSpeed]);

        const buildTopX = uiState.X * 1.5;
        const tmdRelY = uiState.y * 1.5;
        const buildingPolygon = `${-W/2},0 ${W/2},0 ${W/2 + buildTopX},${-H} ${-W/2 + buildTopX},${-H}`;
        const mapGraphY = (val) => 60 - (val * 1.5);
        const graphPathX = uiState.historyX.map((val, i) => `${(i / maxHistory) * 400},${mapGraphY(val)}`).join(' ');
        const graphPathY = uiState.historyY.map((val, i) => `${(i / maxHistory) * 400},${mapGraphY(val)}`).join(' ');

        return (
          <div className="bg-slate-900 text-slate-100 p-4 font-sans rounded-3xl border border-slate-700">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="space-y-4">
                <div className="bg-slate-800 p-4 rounded-2xl border border-slate-700">
                  <h3 className="font-bold text-sky-400 mb-3"><i className="fas fa-wind"></i> 風速控制</h3>
                  <input type="range" min="0" max="10" value={windSpeed} onChange={(e)=>setWindSpeed(parseInt(e.target.value))} className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-sky-500" />
                  <div className="text-right text-xs mt-1">Level {windSpeed}</div>
                  <button onClick={()=>setTmdActive(!tmdActive)} className={`w-full mt-4 py-2 rounded-xl font-bold transition ${tmdActive ? 'bg-amber-500 text-white' : 'bg-slate-700 text-slate-400'}`}>
                    {tmdActive ? "🟡 TMD 已啟動" : "⚪ TMD 已關閉"}
                  </button>
                  <button onClick={()=>setIsPlaying(!isPlaying)} className="w-full mt-2 py-2 bg-slate-600 rounded-xl text-xs">
                    {isPlaying ? "暫停模擬" : "繼續模擬"}
                  </button>
                </div>
                <div className="bg-sky-900/20 p-4 rounded-2xl text-xs text-slate-300 leading-relaxed">
                  <p><strong>💡 物理原理：</strong></p>
                  當風力 $F_{wind}$ 頻率接近 $f_{natural} = \frac{1}{2\pi}\sqrt{\frac{K}{M}}$ 時會產生共振。TMD 會產生反向力來抵銷能量。
                </div>
              </div>
              <div className="lg:col-span-2 space-y-4">
                <div className="bg-slate-800 rounded-2xl border border-slate-700 aspect-video relative overflow-hidden">
                  <svg viewBox="-200 -350 400 400" className="w-full h-full">
                    <rect x="-200" y="0" width="400" height="50" fill="#1e293b" />
                    <polygon points={buildingPolygon} fill="#0f172a" stroke="#64748b" strokeWidth="4" />
                    <circle cx={buildTopX} cy={-H+60} r="30" fill="#1e293b" stroke="#334155" strokeWidth="2" />
                    {tmdActive && (
                      <g>
                        <line x1={buildTopX} y1={-H+30} x2={buildTopX+tmdRelY} y2={-H+60} stroke="#fbbf24" strokeWidth="2" />
                        <circle cx={buildTopX+tmdRelY} cy={-H+60} r="12" fill="#fbbf24" />
                      </g>
                    )}
                    <line x1={buildTopX-W/2} y1={-H+100} x2={buildTopX-W/2 - uiState.windForce*10} y2={-H+100} stroke="#38bdf8" strokeWidth="4" />
                  </svg>
                </div>
                <div className="h-32 bg-slate-900/50 rounded-xl border border-slate-700 p-2">
                  <svg viewBox="0 0 400 120" className="w-full h-full" preserveAspectRatio="none">
                    <line x1="0" y1="60" x2="400" y2="60" stroke="#475569" strokeWidth="1" strokeDasharray="4 4" />
                    <polyline points={graphPathX} fill="none" stroke="#38bdf8" strokeWidth="2" />
                    {tmdActive && <polyline points={graphPathY} fill="none" stroke="#fbbf24" strokeWidth="2" opacity="0.6" />}
                  </svg>
                </div>
              </div>
            </div>
          </div>
        );
      }

      const root = ReactDOM.createRoot(document.getElementById('root'));
      root.render(<SkyscraperSim />);
    </script>
    <style>
      body { margin: 0; background: transparent; overflow: hidden; }
      #root { width: 100%; height: 100%; }
    </style>
    """
    components.html(skyscraper_html, height=800)

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
    st.write("摩天大樓在颱風中如何保持穩定？這背後隱藏著強大的受力分析邏輯。")
    
    # 這裡就是呼叫我們剛才定義的函數
    render_skyscraper_sim()
    
    st.markdown("---")
    st.write("🔍 **羊珞老師的小筆記：**")
    st.write("觀察看看，當你關閉 TMD 時，大樓的擺動幅度是不是明顯變大了？這就是『阻尼』在物理系統中的重要性。")


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
