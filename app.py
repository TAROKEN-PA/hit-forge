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

# --- 2. CSS Style (画面切れ対策強化) ---
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: #101217 !important; color: #ffffff !important; }

      /* ポップアップの幅を広げ、高さを制限し、スクロールを確実にする */
      div[data-testid="stPopoverBody"] {
        background-color: #000000 !important; border: 2px solid #e3b341 !important;
        min-width: 320px !important; /* 幅を確保 */
        max-height: 75vh !important; /* 画面の75%までに制限 */
        overflow-y: auto !important; padding: 15px !important;
      }
      div[data-testid="stPopoverBody"] * { color: #ffffff !important; }

      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; border:none; width:100%; }
      h1, h2, h3, label { color: #ffffff !important; }

      /* ラジオボタンなどの間隔を詰める */
      div[data-testid="stWidgetLabel"] { margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True
)

# --- 3. Sidebar (全ポップアップ統一) ---
with st.sidebar:
    st.markdown('<h1 style="color:#e3b341; font-size:1.6rem; margin-bottom:20px;">🎼 HitForge Menu</h1>',
                unsafe_allow_html=True)

    with st.popover("👤 アーティスト・視点", use_container_width=True):
        v_gender = st.radio("性別", ["Male", "Female", "Non-binary"], index=1)
        l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    with st.popover("📝 制作キーワード", use_container_width=True):
        must_have = st.text_input("必須キーワード")
        negative_p = st.text_input("NGワード")

    with st.popover("📏 文字数制限", use_container_width=True):
        p_limit = st.number_input("最大文字数", 80, 2500, value=1500)

    # --- ジャンル連動ロジック ---
    if "current_bpm" not in st.session_state:
        st.session_state.current_bpm = 148
        st.session_state.current_key = "C#"

    with st.popover("🎹 楽曲構成 (Genre/BPM/Key)", use_container_width=True):
        # 画面を分割して高さを抑える
        def on_genre_change():
            new_dna = DNA_MASTER[st.session_state.genre_radio]
            st.session_state.current_bpm = int(new_dna["bpm"])
            st.session_state.current_key = new_dna["key_name"]


        genre_key = st.radio("1. ジャンル選択", list(DNA_MASTER.keys()), key="genre_radio", on_change=on_genre_change)

        st.markdown("---")
        st.markdown("### 2. 手動微調整")
        # 横並びにして高さを節約
        col1, col2 = st.columns(2)
        with col1:
            user_bpm = st.number_input("BPM", 60, 220, key="current_bpm")
        with col2:
            user_key = st.selectbox("Key", KEY_NAMES, index=KEY_NAMES.index(st.session_state.current_key),
                                    key="current_key_sel")
            st.session_state.current_key = user_key

        dna = DNA_MASTER[genre_key].copy()
        dna["bpm"] = user_bpm
        dna["key_name"] = user_key

    with st.popover("📊 DNA分析結果", use_container_width=True):
        st.write(f"**Logic:** {genre_key}")
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=120)
        key_dist = [0.1] * 12;
        key_dist[KEY_NAMES.index(dna['key_name'])] = 0.9
        st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES), height=120)

    with st.popover("🎨 表現・言語設定", use_container_width=True):
        flavor = st.radio("Flavor", list(LYRIC_FLAVORS.keys()), index=0)
        lang_opt = st.radio("言語", ["日本語（サビ英語）", "全日本語", "韓国語（サビ英語）", "全英語"], index=0)

    st.write("---")
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# --- 4. Main Content ---
st.markdown('<h1 style="color:#e3b341; text-align:center;">🎼 HitForge Production</h1>', unsafe_allow_html=True)
st.markdown('<div style="height:4px; width:180px; background:#e3b341; margin: 0 auto 30px auto;"></div>',
            unsafe_allow_html=True)

if st.button("⚡ GENERATE HIT-DNA PROMPT"):
    style_raw = (
        f"Genre:{genre_key}. BPM:{dna['bpm']}. Key:{dna['key_name']}. Inst:{dna['p']} Vocal:{v_gender}. {'Boost.' if boost_mode else ''}").strip()
    lyrics_raw = (
        f"Lyrics:{genre_key}. Lang:{lang_opt}. POV:{l_pov}. Flavor:{LYRIC_FLAVORS[flavor]}. Theme:{must_have}.").strip()

    st.subheader("🎨 Style Prompt")
    st.text_area("S", style_raw[:p_limit], height=120, label_visibility="collapsed")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("L", lyrics_raw[:p_limit], height=150, label_visibility="collapsed")