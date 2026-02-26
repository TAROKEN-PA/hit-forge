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
#  2. UI Style (ポップアップ内・黒背景・白文字・スクロール)
# =========================================================
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main { background-color: #0a0b0e !important; color: #ffffff !important; }
      [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: #101217 !important; color: #ffffff !important; }

      div[data-testid="stPopoverBody"] {
        background-color: #000000 !important;
        border: 2px solid #e3b341 !important;
        max-height: 80vh !important;
        overflow-y: auto !important;
        padding: 20px !important;
      }
      div[data-testid="stPopoverBody"] * { color: #ffffff !important; }

      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000 !important; font-weight: 900; border-radius: 12px; height: 3.2rem; border:none; width:100%; }
      h1, h2, h3, label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

# =========================================================
#  3. Sidebar (全ポップアップ統一)
# =========================================================
with st.sidebar:
    st.markdown('<h1 style="color:#e3b341; font-size:1.6rem; margin-bottom:20px;">🎼 HitForge Menu</h1>',
                unsafe_allow_html=True)

    # A: アーティスト
    with st.popover("👤 アーティスト・視点", use_container_width=True):
        v_gender = st.radio("性別", ["Male", "Female", "Non-binary"], index=1)
        l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    # B: キーワード
    with st.popover("📝 制作キーワード", use_container_width=True):
        must_have = st.text_input("必須キーワード", placeholder="例: 青い閃光")
        negative_p = st.text_input("NGワード", placeholder="例: 桜")

    # C: 文字数制限 (★スライダーを削除し、入力BOXのみに)
    with st.popover("📏 文字数制限", use_container_width=True):
        p_limit = st.number_input("プロンプト最大文字数", min_value=80, max_value=2500, value=1500, step=10)
        st.caption("※入力した数値がプロンプト生成時に反映されます。")

    # D: ジャンル・BPM・キー設定
    with st.popover("🎹 楽曲構成設定 (BPM/Key)", use_container_width=True):
        genre_key = st.radio("ベースDNAを選択", list(DNA_MASTER.keys()), index=0)
        base_dna = DNA_MASTER[genre_key]
        st.write("---")
        st.markdown("### 🎛️ 手動微調整")
        user_bpm = st.slider("BPM (テンポ)", 60, 220, int(base_dna["bpm"]))
        user_key = st.selectbox("Key (調)", KEY_NAMES, index=base_dna["key"])
        dna = base_dna.copy()
        dna["bpm"] = user_bpm
        dna["key_name"] = user_key

    # E: DNA分析
    with st.popover("📊 現在のDNA分析結果", use_container_width=True):
        st.write(f"### DNA Logic: {genre_key}")
        bpm_bins = np.linspace(60, 200, 15)
        bpm_dist = np.exp(-0.5 * ((bpm_bins - dna['bpm']) / 15) ** 2)
        st.bar_chart(pd.DataFrame({'Freq': bpm_dist}, index=bpm_bins.astype(int)), height=150)
        current_key_idx = KEY_NAMES.index(user_key)
        key_dist = [0.1] * 12;
        key_dist[current_key_idx] = 0.9
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
    st.text_area("S", style_raw[:p_limit], height=140, label_visibility="collapsed")
    st.write("---")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("L", lyrics_raw[:p_limit], height=200, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)