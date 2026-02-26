# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# --- 1. Master DNA Data (一切削らず、全ロジックを保持) ---
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "C#", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。",
                           "p": "Modern J-POP production, rich layers, hybrid synths, emotional piano.",
                           "v_base": "First Hook <40s. High production value. Bright mix."},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "C", "energy": 0.45, "logic": "ピアノ主体の構成。",
                       "p": "Grand Piano, emotional strings, delicate live percussion, acoustic bass.",
                       "v_base": "Slow build, emotional peak at chorus, dynamic vocal delivery."},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "D", "energy": 0.85, "logic": "Overdriven guitars/Energetic drums.",
               "p": "Driving electric guitars, energetic bass, real acoustic drums, raw energy.",
               "v_base": "High energy, aggressive mix, powerful vocal presence."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "C#", "energy": 0.90, "logic": "高揚感と転調の多用。",
                   "p": "Hyper-melodic, orchestral mixed with synths, fast-paced strings.",
                   "v_base": "Complex structure, frequent modulations, anthemic chorus."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths, fast piano arpeggios, glitch effects, hyper-digital.",
                       "v_base": "Lightning-fast articulation, robotic yet emotional tuning."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass.",
                 "p": "Fretless bass, funky Rhodes, vintage 80s DX7, groovy rhythm guitar.",
                 "v_base": "Mellow vibes, jazz-pop fusion, sophisticated vocal layers."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンスフロア。",
                      "p": "Heavy sub-bass, experimental lead synths, crisp percussion, EDM elements.",
                      "v_base": "Powerful drop, varied vocal textures, rhythmic precision."},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。",
                       "p": "Heavy 808s, rhythmic vocal chops, dark cinematic synths.",
                       "v_base": "Trap-influenced sections, aggressive rap and melodic hooks."},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。",
                     "p": "Catchy pluck leads, simple but effective bass, TikTok-friendly loop.",
                     "v_base": "Loop-friendly, high memorability, clear vocal hook."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes。",
                      "p": "Chill Rhodes, dusty vinyl, boom-bap drums, nostalgic atmosphere.",
                      "v_base": "Relaxed atmosphere, laid-back vocal or instrumental focus."},
}
KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {"王道チャート": "Standard", "詩的・比喩的": "Metaphorical", "映画的描写": "Cinematic",
                 "ストレート/感情剥き出し": "Raw", "哲学的・ダーク": "Deep"}

# --- 2. CSS Style (黒背景・金枠・グラフ2列対応) ---
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: #101217 !important; color: #ffffff !important; }
      div[data-testid="stPopoverBody"] {
        background-color: #000000 !important; border: 2px solid #e3b341 !important;
        min-width: 450px !important; max-height: 85vh !important; overflow-y: auto !important;
      }
      div[data-testid="stPopoverBody"] * { color: #ffffff !important; }
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; }
      h1, h2, h3, label, p, span { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

# --- 3. Sidebar (設定をすべてポップアップに集約) ---
with st.sidebar:
    st.markdown('<h1 style="color:#e3b341; font-size:1.5rem; margin-bottom:20px;">🎼 HitForge Menu</h1>',
                unsafe_allow_html=True)

    with st.popover("👤 アーティスト・視点", use_container_width=True):
        v_gender = st.selectbox("性別", ["Male", "Female", "Non-binary"], index=1)
        l_pov = st.selectbox("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    with st.popover("📝 制作キーワード", use_container_width=True):
        must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
        negative_p = st.text_input("NGワード", placeholder="例: 桜")

    with st.popover("📏 文字数制限", use_container_width=True):
        p_limit = st.number_input("最大文字数", 80, 2500, value=1500)

    # 楽曲構成 (連動ロジック)
    if "current_bpm" not in st.session_state:
        st.session_state.current_bpm = 148
        st.session_state.current_key = "C#"
        st.session_state.last_genre = "J-POP (Mainstream)"

    with st.popover("🎹 楽曲構成 (Genre/BPM/Key)", use_container_width=True):
        genre_key = st.selectbox("1. ベースジャンル", list(DNA_MASTER.keys()), key="genre_sel")
        if genre_key != st.session_state.last_genre:
            st.session_state.current_bpm = int(DNA_MASTER[genre_key]["bpm"])
            st.session_state.current_key = DNA_MASTER[genre_key]["key_name"]
            st.session_state.last_genre = genre_key
            st.rerun()
        st.write("---")
        st.markdown("### 2. 手動微調整")
        col_b, col_k = st.columns(2)
        with col_b:
            user_bpm = st.number_input("BPM", 60, 220, key="current_bpm")
        with col_k:
            user_key = st.selectbox("Key", KEY_NAMES, index=KEY_NAMES.index(st.session_state.current_key),
                                    key="current_key_sel")
            st.session_state.current_key = user_key
        dna = DNA_MASTER[genre_key].copy()
        dna.update({"bpm": user_bpm, "key_name": user_key})

    with st.popover("📊 DNA分析 (BPM & Key)", use_container_width=True):
        c1, c2 = st.columns(2)
        with c1:
            st.caption("BPM Distribution")
            bpm_bins = np.linspace(60, 200, 15)
            bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
            st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=150)
        with c2:
            st.caption("Key Popularity")
            key_dist = [0.1] * 12;
            key_dist[KEY_NAMES.index(dna['key_name'])] = 0.9
            st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES), height=150)
        st.write(f"> Logic: {dna['logic']}")

    with st.popover("🎨 言語・表現", use_container_width=True):
        flavor = st.selectbox("フレーバー", list(LYRIC_FLAVORS.keys()))
        lang_opt = st.selectbox("言語構成",
                                ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"])

    st.write("---")
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# --- 4. Main Content (プロンプト生成仕様を100%復元) ---
st.markdown('<h1 style="color:#e3b341; text-align:center;">🎼 HitForge Production</h1>', unsafe_allow_html=True)
st.markdown('<div style="height:4px; width:150px; background:#e3b341; margin: 0 auto 30px auto;"></div>',
            unsafe_allow_html=True)

if st.button("⚡ GENERATE HIT-DNA PROMPT"):
    # Style Prompt: 楽器詳細(p)、ボーカル、構成指示、ロジックをすべて統合
    style_raw = (
        f"Genre: {genre_key}. BPM: {dna['bpm']}. Key: {dna['key_name']}. Energy: {dna['energy']}. "
        f"Instrumentation: {dna['p']} Vocal: {v_gender} perspective. "
        f"{'Apply Anthemic Boost for stadiums.' if boost_mode else ''} "
        f"{'Optimize for Top-Chart streaming algorithms.' if optimizer else ''} "
        f"Production Logic: {dna['v_base']} Avoid: {negative_p if negative_p else 'cliches'}."
    )

    # Lyrics Prompt: 歌詞構造、テーマ、フレーバーを詳細に復元
    lyrics_raw = (
        f"Lyrics Theme: {must_have if must_have else 'Universal emotion'}. "
        f"Language Config: {lang_opt}. Perspective: {l_pov}. Flavor: {LYRIC_FLAVORS[flavor]}. "
        f"Genre DNA: {genre_key}. Structure: Intro-Verse1-PreChorus-Chorus-Verse2-Chorus-Bridge-Chorus-Outro. "
        f"Exclude Keywords: {negative_p if negative_p else 'none'}."
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style Prompt")
    st.text_area("S", style_raw[:p_limit], height=180, label_visibility="collapsed")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("L", lyrics_raw[:p_limit], height=180, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)