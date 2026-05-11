import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

# ==========================================
# 1. 設計圖區 (定義區)：摩天大樓模擬器
# ==========================================
def render_skyscraper_sim():
    """
    將 React 摩天大樓模擬器封裝為 Streamlit 組件，包含內嵌的 Gemini 連結按鈕
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
          <div className="bg-slate-900 text-slate-100 p-6 font-sans rounded-3xl border border-slate-700 shadow-2xl">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="space-y-6">
                <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700">
                  <h3 className="font-bold text-sky-400 mb-4"><i className="fas fa-sliders-h"></i> 環境控制</h3>
                  <div className="space-y-4">
                    <label className="text-xs text-slate-400 uppercase tracking-wider">颱風風速 (Level)</label>
                    <input type="range" min="0" max="10" value={windSpeed} onChange={(e)=>setWindSpeed(parseInt(e.target.value))} className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-sky-500" />
                    <div className="text-right text-sky-300 font-mono">Level {windSpeed}</div>
                  </div>
                  
                  <button onClick={()=>setTmdActive(!tmdActive)} className={`w-full mt-6 py-3 rounded-xl font-bold transition-all ${tmdActive ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/20' : 'bg-slate-700 text-slate-400'}`}>
                    {tmdActive ? "🟡 TMD 已啟動" : "⚪ TMD 已關閉"}
                  </button>

                  <a href="https://gemini.google.com/share/532b796fbbc6" target="_blank" className="block w-full mt-4 py-3 bg-sky-600/20 hover:bg-sky-600/40 border border-sky-500/50 rounded-xl text-center text-sky-300 text-sm font-bold transition-all no-underline">
                    <i className="fas fa-robot mr-2"></i> 查看 Gemini 邏輯筆記
                  </a>
                </div>
                <div className="bg-sky-900/20 p-4 rounded-2xl text-xs text-slate-300 leading-relaxed border border-sky-500/10">
                  <p><strong>💡 物理小科普：</strong></p>
                  當風力頻率接近大樓的自然頻率時，會產生「共振」。這顆重達數百噸的黃色 TMD 會朝反方向擺動，吸收大樓的動能！
                </div>
              </div>
              
              <div className="lg:col-span-2 space-y-6">
                <div className="bg-slate-800 rounded-2xl border border-slate-700 aspect-video relative overflow-hidden shadow-inner">
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
                <div className="h-32 bg-slate-950 rounded-xl border border-slate-700 p-2">
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
      body { margin: 0; background: transparent; }
      #root { width: 100%; }
    </style>
    """
    components.html(skyscraper_html, height=850)

# ==========================================
# 2. 系統配置區 (帳號與身分)
# ==========================================
st.set_page_config(page_title="物理漫遊天地 | 羊珞老師", page_icon="🐑", layout="wide")

USER_DB = {
    "admin": {"pw": "yangluo888", "name": "羊珞老師", "role": "老師"},
    "S001": {"pw": "physics123", "name": "林同學", "role": "學生", "progress": 85},
    "S002": {"pw": "physics123", "name": "王同學", "role": "學生", "progress": 40},
}

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "遊客"
    st.session_state['user_name'] = "一般遊客"

# ==========================================
# 3. 側邊欄 (登入與視覺)
# ==========================================
with st.sidebar:
    st.title("🐑 物理漫遊天地")
    
    # 羊珞老師小動畫
    st.markdown("""
    <svg width="100" height="100" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="30" fill="#f8f9fa" stroke="#005088" stroke-width="2">
        <animate attributeName="r" values="30;32;30" dur="3s" repeatCount="indefinite" />
      </circle>
      <text x="35" y="55" font-family="Arial" font-size="10" fill="#005088">咩~ Science</text>
    </svg>
    """, unsafe_allow_html=True)
    
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
                st.error("驗證失敗，請檢查帳密。")
    else:
        st.write(f"當前身分：**{st.session_state['user_role']}**")
        st.write(f"歡迎回來，{st.session_state['user_name']}")
        if st.button("登出系統"):
            st.session_state['user_role'] = "遊客"
            st.rerun()

# ==========================================
# 4. 主選單路由
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

selected = option_menu(None, options=menu, icons=icons, orientation="horizontal",
                       styles={"container": {"padding": "0!important", "background-color": "#f8f9fa"}})

# ==========================================
# 5. 分頁內容執行
# ==========================================

if selected == "物理新知":
    st.header("✨ 物理漫遊：建築中的減震魔法")
    st.write("摩天大樓在強風中為何能屹立不搖？讓我們透過這份互動模擬來觀察 **調諧質量阻尼器 (TMD)** 的威力。")
    
    # 呼叫最上方定義好的函數
    render_skyscraper_sim()

elif selected == "PhET實驗室":
    st.header("🔬 官方互動模擬器")
    st.write("這裡是連結 PhET 的視窗，嘗試手動操作各種物理量。")
    components.iframe("https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_all.html", height=600)

elif selected == "我的進度":
    uid = st.session_state['current_uid']
    st.header(f"📊 {st.session_state['user_name']} 的學習軌跡")
    prog = USER_DB[uid]["progress"]
    st.progress(prog / 100)
    st.write(f"本學期物理專題完成率：{prog}%")

elif selected == "Google Classroom":
    st.header("🏫 教學連動系統")
    st.write("請跳轉至 Google Classroom 查看最新講義與派發的作業。")
    st.link_button("🚀 前往 Classroom", "https://classroom.google.com")

elif selected == "教師後台":
    st.header("👁️ 羊珞老師的戰略後台")
    st.write("目前班級學生的登入狀態與學習數據。")
    st.table(USER_DB)

# 頁尾
st.markdown("---")
st.caption("© 2026 物理漫遊天地 - 羊珞老師版權所有 | 邏輯、溫柔與 AI 的結晶。咩～🐑")
