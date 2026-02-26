# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================================================
#  1. Master DNA Data (全データ保持)
# =========================================================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。",
                           "p": "Modern J-POP production, rich layers, hybrid synths.",
                           "v_base": "First Hook <40s. High production value."},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。",
                       "p": "Grand Piano, emotional strings, delicate live percussion.",
                       "v_base": "Slow build, emotional peak at chorus."},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars/Energetic drums.",
               "p": "Driving electric guitars, energetic bass, real acoustic drums.",
               "v_base": "High energy, aggressive mix."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調の多用。",
                   "p": "Hyper-melodic, fast-paced, orchestral elements mixed with synths.",
                   "v_base": "Complex structure, frequent modulations."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths, fast piano arpeggios, glitch effects.",
                       "v_base": "Lightning-fast articulation, robotic precision."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass.",
                 "p": "Fretless bass, funky Rhodes, vintage 80s DX7 synth pads, clean electric guitar.",
                 "v_base": "Mellow vibes, sophisticated jazz-pop fusion."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンスフロア。",
                      "p": "Heavy sub-bass, experimental sound design, sharp lead synths.",
                      "v_base": "Powerful drop, varied vocal textures."},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。",
                       "p": "Heavy 808s, rhythmic vocal chops, dark atmospheric pads.",
                       "v_base": "Trap-influenced, aggressive rap sections."},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。",
                     "p": "Catchy pluck leads, simple but effective bass, organic percussion.",
                     "v_base": "Loop-friendly, high memorability."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes。",
                      "p": "Chill Rhodes, dusty vinyl crackle, boom-bap drums, sampled aesthetic.",
                      "v_base": "Relaxed atmosphere, nostalgic mood."},
}
KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {"王道チャート": "Standard", "詩的・比喩的": "Metaphorical", "映画的描写": "Cinematic",
                 "ストレート/感情剥き出し": "Raw", "哲学的・ダーク": "Deep"}

# =========================================================
#  2. UI Style (はみ出し対策スクロールCSS追加)
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: #101217 !important; color: #ffffff !important; }
      button[kind="header"] svg { fill: #ffffff !important; stroke: #ffffff !important; }

      /* ポップアップ(Popover)のはみ出し対策 */
      div[data-testid="stPopoverBody"] {
        background-color: #000000 !important;
        border: 2px solid #e3b341 !important;
        max-height: 80vh !important; /* 画面の高さの80%までに制限 */
        overflow-y: auto !important; /* 縦スクロールを有効に */
        box-shadow: 0px 4px 20px rgba(0,0,0,0.8) !important;
      }
      div[data-testid="stPopoverBody"] * { color: #ffffff !important; }

      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; border:none; width:100%; }
      h1, h2, h3, label, p { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

# =========================================================
#  3. Sidebar (全ポップアップ統一)
# =========================================================
with st.sidebar:
    st.markdown('<h1 style="color:#e3b341; font-size:1.6rem;">🎼 HitForge Menu</h1>', unsafe_allow_html=True)

    with st.popover("👤 アーティスト・視点", use_container_width=True):
        v_gender = st.radio("性別", ["Male", "Female", "Non-binary"], index=1)
        l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    with st.popover("📝 制作キーワード", use_container_width=True):
        must_have = st.text_input("必須キーワード")
        negative_p = st.text_input("NGワード")

    with st.popover("📏 文字数制限", use_container_width=True):
        if "p_limit" not in st.session_state: st.session_state.p_limit = 1500
        st.number_input("Value", 80, 2500, key="n_in",
                        on_change=lambda: st.session_state.update(p_limit=st.session_state.n_in),
                        value=st.session_state.p_limit)
        st.slider("Slider", 80, 2500, key="s_in",
                  on_change=lambda: st.session_state.update(p_limit=st.session_state.s_in),
                  value=st.session_state.p_limit)

    with st.popover("🎹 ジャンル・DNA分析", use_container_width=True):
        # ここがスクロールされるようになるお！
        genre_key = st.radio("DNA Genre", list(DNA_MASTER.keys()), index=0)
        dna = DNA_MASTER[genre_key]
        st.write(f"**DNA Logic:** {dna['logic']}")
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=150)
        key_dist = [0.1] * 12;
        key_dist[dna['key']] = 0.9
        st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES), height=150)

    with st.popover("🎨 表現・言語設定", use_container_width=True):
        flavor = st.radio("Lyricフレーバー", list(LYRIC_FLAVORS.keys()), index=0)
        lang_opt = st.radio("言語構成",
                            ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"], index=0)

    st.write("---")
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================================================
#  4. Main Content
# =========================================================
st.markdown('<h1 style="color:#e3b341; text-align:center; font-size:2.2rem;">🎼 HitForge Production</h1>',
            unsafe_allow_html=True)
st.markdown(
    '<div style="height:4px; width:150px; background:linear-gradient(90deg, #e3b341, #f1c84c); margin: 0 auto 30px auto; border-radius:6px;"></div>',
    unsafe_allow_html=True)

if st.button("⚡ GENERATE HIT-DNA PROMPT"):
    style_raw = f"Genre:{genre_key}.BPM:{dna['bpm']}.Inst:{dna['p']}Vocal:{v_gender}."
    lyrics_raw = f"Lyrics:{genre_key}.Lang:{lang_opt}.Flavor:{flavor}.Theme:{must_have}."

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style / Composition")
    st.text_area("S", style_raw[:st.session_state.p_limit], height=120, label_visibility="collapsed")
    st.subheader("✍️ Lyrics")
    st.text_area("L", lyrics_raw[:st.session_state.p_limit], height=180, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)