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
                   "p": "Hyper-melodic, orchestral mixed with synths.",
                   "v_base": "Complex structure, frequent modulations."},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "F#", "energy": 0.92, "logic": "超高速/複雑。",
                       "p": "Aggressive digital synths, fast piano arpeggios, glitch effects.",
                       "v_base": "Lightning-fast articulation."},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "A", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass.",
                 "p": "Fretless bass, funky Rhodes, vintage 80s DX7.", "v_base": "Mellow vibes, jazz-pop fusion."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "C#", "energy": 0.82, "logic": "低音重視ダンスフロア。",
                      "p": "Heavy sub-bass, experimental lead synths.",
                      "v_base": "Powerful drop, varied vocal textures."},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "Bb", "energy": 0.75, "logic": "重厚Trapビート。",
                       "p": "Heavy 808s, rhythmic vocal chops.", "v_base": "Trap-influenced sections."},
    "Global Viral": {"bpm": 105, "key": 7, "key_name": "G", "energy": 0.72, "logic": "王道Viral。",
                     "p": "Catchy pluck leads, simple but effective bass.",
                     "v_base": "Loop-friendly, high memorability."},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "F", "energy": 0.35, "logic": "Vinyl crackle/Rhodes。",
                      "p": "Chill Rhodes, dusty vinyl, boom-bap drums.", "v_base": "Relaxed atmosphere."},
}
KEY_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
LYRIC_FLAVORS = {"王道チャート": "Standard", "詩的・比喩的": "Metaphorical", "映画的描写": "Cinematic",
                 "ストレート/感情剥き出し": "Raw", "哲学的・ダーク": "Deep"}

# =========================================================
#  2. UI Style (ポップアップ内視認性・スクロール強化)
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: #101217 !important; color: #ffffff !important; }
      button[kind="header"] svg { fill: #ffffff !important; stroke: #ffffff !important; }

      /* ポップアップ(Popover)の強制スタイル */
      div[data-testid="stPopoverBody"] {
        background-color: #000000 !important;
        border: 2px solid #e3b341 !important;
        max-height: 70vh !important; /* 高さを少し抑えて確実に表示 */
        overflow-y: auto !important;
        padding: 20px !important;
      }
      /* 全ブラウザでポップアップ内を白文字に固定 */
      div[data-testid="stPopoverBody"] label, 
      div[data-testid="stPopoverBody"] p, 
      div[data-testid="stPopoverBody"] span,
      div[data-testid="stPopoverBody"] h3,
      div[data-testid="stPopoverBody"] div {
        color: #ffffff !important;
      }

      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; border:none; width:100%; }
      h1, h2, h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

# =========================================================
#  3. Sidebar (全ポップアップ・分離設計)
# =========================================================
with st.sidebar:
    st.markdown('<h1 style="color:#e3b341; font-size:1.6rem; margin-bottom:20px;">🎼 HitForge Menu</h1>',
                unsafe_allow_html=True)

    # A: アーティスト設定
    with st.popover("👤 アーティスト・視点", use_container_width=True):
        v_gender = st.radio("性別", ["Male", "Female", "Non-binary"], index=1)
        l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    # B: キーワード
    with st.popover("📝 制作キーワード", use_container_width=True):
        must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
        negative_p = st.text_input("NGワード", placeholder="例: 桜")

    # C: 文字数
    with st.popover("📏 文字数制限", use_container_width=True):
        if "p_limit" not in st.session_state: st.session_state.p_limit = 1500


        def sync_n(): st.session_state.p_limit = st.session_state.n_in


        def sync_s(): st.session_state.p_limit = st.session_state.s_in


        st.number_input("Value", 80, 2500, key="n_in", on_change=sync_n, value=st.session_state.p_limit)
        st.slider("Slider", 80, 2500, key="s_in", on_change=sync_s, value=st.session_state.p_limit)

    # D: ジャンル選択 (ここを単体化してコンパクトに)
    with st.popover("🎹 楽曲ジャンル選択", use_container_width=True):
        genre_key = st.radio("DNA Genre", list(DNA_MASTER.keys()), index=0)
        dna = DNA_MASTER[genre_key]
        st.success(f"Selected: {genre_key}")

    # E: DNA分析 (グラフ専用に分離)
    with st.popover("📊 現在のDNA分析結果", use_container_width=True):
        st.write(f"### DNA Logic: {genre_key}")
        st.write(f"> {dna['logic']}")

        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.caption("BPM Distribution")
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=150)

        key_dist = [0.1] * 12;
        key_dist[dna['key']] = 0.9
        st.caption("Key Popularity")
        st.bar_chart(pd.DataFrame({'Pop': key_dist}, index=KEY_NAMES), height=150)

    # F: 言語・表現
    with st.popover("🎨 表現・言語設定", use_container_width=True):
        flavor = st.radio("Lyricフレーバー", list(LYRIC_FLAVORS.keys()), index=0)
        lang_opt = st.radio("言語構成",
                            ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"], index=0)

    st.write("---")
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================================================
#  4. Main Display
# =========================================================
st.markdown('<h1 style="color:#e3b341; text-align:center; font-size:2.5rem;">🎼 HitForge Production</h1>',
            unsafe_allow_html=True)
st.markdown(
    '<div style="height:4px; width:180px; background:#e3b341; margin: 0 auto 30px auto; border-radius:6px;"></div>',
    unsafe_allow_html=True)

if st.button("⚡ GENERATE HIT-DNA PROMPT"):
    style_raw = (
        f"Genre:{genre_key}.BPM:{dna['bpm']}.Key:{dna['key_name']}.Energy:{dna['energy']}.Inst:{dna['p']}Vocal:{v_gender}.{'Anthemic boost.' if boost_mode else ''}{'Chart Opt.' if optimizer else ''}{dna['v_base']}Avoid:{negative_p if negative_p else 'none'}.").strip()
    lyrics_raw = (
        f"Lyrics:{genre_key}.Lang:{lang_opt}.POV:{l_pov}.Flavor:{LYRIC_FLAVORS[flavor]}.Theme:{must_have}.Exclude:{negative_p if negative_p else 'none'}.Struct:In-V1-PC-C-V2-C-B-C-Out.").strip()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style Prompt")
    st.text_area("S", style_raw[:st.session_state.p_limit], height=140, label_visibility="collapsed")
    st.button("📋 Copy Style", on_click=lambda: st.write(
        f'<script>navigator.clipboard.writeText("{style_raw[:st.session_state.p_limit]}")</script>',
        unsafe_allow_html=True), key="cp_s")
    st.write("---")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("L", lyrics_raw[:st.session_state.p_limit], height=200, label_visibility="collapsed")
    st.button("📋 Copy Lyrics", on_click=lambda: st.write(
        f'<script>navigator.clipboard.writeText("{lyrics_raw[:st.session_state.p_limit]}")</script>',
        unsafe_allow_html=True), key="cp_l")
    st.markdown('</div>', unsafe_allow_html=True)