# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# --- 1. Master DNA Data ---
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78, "logic": "現代の王道ヒット。",
                           "p": "Modern J-POP production.", "v_base": "First Hook <40s."},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。",
                       "p": "Grand Piano, strings.", "v_base": "Slow build."},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars.",
               "p": "Driving guitars, drums.", "v_base": "High energy."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調多用。",
                   "p": "Orchestral mixed with synths.", "v_base": "Complex structure."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths.", "v_base": "Fast articulation."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7/Fretless bass.",
                 "p": "Fretless bass, Rhodes.", "v_base": "Mellow vibes."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンス。",
                      "p": "Heavy sub-bass, synths.", "v_base": "Powerful drop."},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。",
                       "p": "Heavy 808s, vocal chops.", "v_base": "Trap style."},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。",
                     "p": "Catchy leads, simple bass.", "v_base": "Loop-friendly."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes。",
                      "p": "Chill Rhodes, dusty vinyl.", "v_base": "Relaxed mood."},
}
KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {"王道チャート": "Standard", "詩的・比喩的": "Metaphorical", "映画的描写": "Cinematic",
                 "ストレート": "Raw", "哲学的": "Deep"}

# --- 2. CSS Style (ポップアップ内の視覚的安定性を最優先) ---
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: #101217 !important; color: #ffffff !important; }

      div[data-testid="stPopoverBody"] {
        background-color: #000000 !important; border: 2px solid #e3b341 !important;
        min-width: 350px !important; max-height: 70vh !important; overflow-y: auto !important; padding: 20px !important;
      }
      /* 全要素を白文字に、ウィジェット背景をダークに */
      div[data-testid="stPopoverBody"] * { color: #ffffff !important; }
      div[data-testid="stPopoverBody"] div[data-baseweb="select"] > div { background-color: #1a1a1a !important; border-color: #444 !important; }

      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; }
      h1, h2, h3, label { color: #ffffff !important; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True
)

# --- 3. Sidebar (全ポップアップ統一) ---
with st.sidebar:
    st.markdown('<h1 style="color:#e3b341; font-size:1.5rem; margin-bottom:20px;">🎼 HitForge Menu</h1>',
                unsafe_allow_html=True)

    # A: 属性
    with st.popover("👤 アーティスト・視点", use_container_width=True):
        v_gender = st.selectbox("性別", ["Male", "Female", "Non-binary"], index=1)
        l_pov = st.selectbox("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    # B: 制作キーワード
    with st.popover("📝 制作キーワード", use_container_width=True):
        must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
        negative_p = st.text_input("NGワード", placeholder="例: 桜")

    # C: 文字数
    with st.popover("📏 文字数制限", use_container_width=True):
        p_limit = st.number_input("最大文字数", 80, 2500, value=1500)

    # D: 楽曲構成 (ここをドロップダウンにして省スペース化)
    if "current_bpm" not in st.session_state:
        st.session_state.current_bpm = 148
        st.session_state.current_key = "C#"
        st.session_state.last_genre = "J-POP (Mainstream)"

    with st.popover("🎹 楽曲構成 (Genre/BPM/Key)", use_container_width=True):
        # 縦に伸びないようにセレクトボックスを採用
        genre_key = st.selectbox("1. ベースジャンル", list(DNA_MASTER.keys()), key="genre_sel")

        # ジャンル変更時の自動連動
        if genre_key != st.session_state.last_genre:
            st.session_state.current_bpm = int(DNA_MASTER[genre_key]["bpm"])
            st.session_state.current_key = DNA_MASTER[genre_key]["key_name"]
            st.session_state.last_genre = genre_key
            st.rerun()

        st.markdown("---")
        st.markdown("### 2. 手動微調整")
        col1, col2 = st.columns(2)
        with col1:
            user_bpm = st.number_input("BPM", 60, 220, key="current_bpm")
        with col2:
            user_key = st.selectbox("Key", KEY_NAMES, index=KEY_NAMES.index(st.session_state.current_key),
                                    key="current_key_sel")
            st.session_state.current_key = user_key

        dna = DNA_MASTER[genre_key].copy()
        dna.update({"bpm": user_bpm, "key_name": user_key})

    # E: 分析
    with st.popover("📊 DNA分析", use_container_width=True):
        st.write(f"**Selected:** {genre_key}")
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=120)

    # F: 言語
    with st.popover("🎨 言語・表現", use_container_width=True):
        flavor = st.selectbox("フレーバー", list(LYRIC_FLAVORS.keys()))
        lang_opt = st.selectbox("言語構成", ["日本語（サビ英語）", "全日本語", "韓国語（サビ英語）", "全英語"])

    st.write("---")
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# --- 4. Main Display ---
st.markdown('<h1 style="color:#e3b341; text-align:center;">🎼 HitForge Production</h1>', unsafe_allow_html=True)
st.markdown('<div style="height:4px; width:150px; background:#e3b341; margin: 0 auto 30px auto;"></div>',
            unsafe_allow_html=True)

if st.button("⚡ GENERATE HIT-DNA PROMPT"):
    style_p = f"Genre:{genre_key}. BPM:{dna['bpm']}. Key:{dna['key_name']}. Inst:{dna['p']} Vocal:{v_gender}."
    lyric_p = f"Lyrics:{genre_key}. Lang:{lang_opt}. POV:{l_pov}. Flavor:{flavor}. Theme:{must_have}."

    st.subheader("🎨 Style Prompt")
    st.text_area("S", style_p[:p_limit], height=120, label_visibility="collapsed")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("L", lyric_p[:p_limit], height=150, label_visibility="collapsed")