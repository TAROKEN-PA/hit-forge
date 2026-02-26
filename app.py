# -*- coding: utf-8 -*-
import streamlit as st

APP_TITLE = "HitForge"
st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="expanded")

# =========================
#  HitForge Master DNA Data
# =========================
DNA_MASTER = {
    "J-POP (Mainstream)": {"bpm": 148, "key": 1, "key_name": "1 (C#/Db)", "energy": 0.78,
                           "logic": "現代の王道ヒット。BPM140超の疾走感。"},
    "J-POP (Ballad)": {"bpm": 72, "key": 0, "key_name": "0 (C)", "energy": 0.45, "logic": "ピアノ主体の構成。"},
    "J-Rock": {"bpm": 165, "key": 2, "key_name": "2 (D)", "energy": 0.85,
               "logic": "Overdriven guitars/Energetic drums."},
    "Anime Song": {"bpm": 175, "key": 1, "key_name": "1 (C#/Db)", "energy": 0.90, "logic": "高揚感と転調の多用。"},
    "Vocaloid Style": {"bpm": 190, "key": 6, "key_name": "6 (F#/Gb)", "energy": 0.92, "logic": "超高速/複雑。"},
    "City Pop": {"bpm": 115, "key": 9, "key_name": "9 (A)", "energy": 0.65, "logic": "80s DX7 synths/Fretless bass."},
    "K-Pop (Dance)": {"bpm": 124, "key": 1, "key_name": "1 (C#/Db)", "energy": 0.82, "logic": "低音重視ダンスフロア。"},
    "K-Pop (HipHop)": {"bpm": 95, "key": 10, "key_name": "10 (A#/Bb)", "energy": 0.75, "logic": "重厚Trapビート。"},
    "Global Viral)": {"bpm": 105, "key": 7, "key_name": "7 (G)", "energy": 0.72, "logic": "王道Viral。"},
    "Lo-fi Hip Hop": {"bpm": 85, "key": 5, "key_name": "5 (F)", "energy": 0.35, "logic": "Vinyl crackle/Rhodes."},
    "Future Bass": {"bpm": 160, "key": 1, "key_name": "1 (C#/Db)", "energy": 0.85, "logic": "キラキラしたシンセ音。"},
    "Trap": {"bpm": 140, "key": 8, "key_name": "8 (G#/Ab)", "energy": 0.75, "logic": "808ベースの唸り。"},
}

KEY_LIST = ["0 (C)", "1 (C#/Db)", "2 (D)", "3 (D#/Eb)", "4 (E)", "5 (F)",
            "6 (F#/Gb)", "7 (G)", "8 (G#/Ab)", "9 (A)", "10 (A#/Bb)", "11 (B)"]

# =========================
#  Lux UI: Browser Neutral Fix (強制色指定)
# =========================
st.markdown(
    """
    <style>
      /* 全体背景と基本文字色を強制 */
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #0a0b0e !important;
        color: #ffffff !important;
      }
      [data-testid="stSidebar"] {
        background-color: #101217 !important;
        border-right: 1px solid #1d212a !important;
      }
      /* 入力フォームの背景と文字色を強制(ブラウザ依存対策) */
      input, select, textarea, div[data-baseweb="select"], .stNumberInput div {
        background-color: #1d212a !important;
        color: #ffffff !important;
        border-color: #333 !important;
      }
      /* 全ラベルの文字色を白に強制 */
      label, p, span, h1, h2, h3, small {
        color: #ffffff !important;
      }
      .app-title h1 { font-size: 2.6rem; font-weight: 900; margin: 0; }
      .gold-underline { display:inline-block; height:6px; width:160px; border-radius:6px; background: linear-gradient(90deg, #e3b341, #f1c84c); margin-bottom: 20px; }
      .card { background-color: #111418 !important; border: 1px solid #1d212a !important; border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem; }
      .stButton > button { background: linear-gradient(135deg, #1b1e25 0%, #e3b341 100%) !important; color:#000000 !important; font-weight: 900; border-radius: 12px; border:none; width:100%; height: 3.2rem; }
      .gold-chip { display:inline-flex; background: rgba(227,179,65,0.15); border:1px solid #e3b341; padding:2px 10px; border-radius: 20px; color: #e3b341 !important; font-size:0.8rem; margin-right:5px; }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="app-title"><h1>🎼 HitForge</h1><span class="gold-underline"></span></div>',
            unsafe_allow_html=True)

# =========================
#  Sidebar (Controls)
# =========================
with st.sidebar:
    st.header("👤 IDENTITY")
    v_gender = st.radio("アーティスト性別", ["Male", "Female", "Non-binary"], index=1)
    l_pov = st.radio("歌詞の視点", ["Male POV", "Female POV", "Neutral POV"], index=2)

    st.header("📝 PRODUCTION")
    must_have = st.text_input("歌詞必須キーワード", placeholder="例: 青い閃光")
    negative_p = st.text_input("NGワード", placeholder="例: 卒業, 桜")

    st.write("プロンプト文字数制限")
    c1, c2 = st.columns([2, 1])
    with c1:
        limit_sl = st.slider("Slider", 80, 2500, 1500, 10, label_visibility="collapsed")
    with c2:
        limit = st.number_input("Value", 80, 2500, value=limit_sl, label_visibility="collapsed")

    st.header("🎛️ DNA PRESET")
    genre_key = st.selectbox("GENRE (Preset)", list(DNA_MASTER.keys()))
    dna = DNA_MASTER[genre_key]

    # --- グラフ表示ボタンを追加 ---
    if st.button("📊 Show DNA Stats (グラフ確認)"):
        st.write(f"**Current DNA: {genre_key}**")
        # BPM グラフ (簡易表示)
        st.caption(f"BPM Position: {dna['bpm']}")
        st.progress((dna['bpm'] - 40) / 260)  # 40-300の範囲で可視化
        # Key Position (0-11)
        st.caption(f"Key Position: {dna['key_name']}")
        st.bar_chart([0 if i != dna['key'] else dna['energy'] for i in range(12)])

    manual_on = st.toggle("🔧 Manual Overide (手動調整)")
    if manual_on:
        t_bpm = st.number_input("BPM", 40, 300, value=dna["bpm"])
        t_key = st.selectbox("KEY", KEY_LIST, index=KEY_LIST.index(dna["key_name"]))
    else:
        t_bpm = dna["bpm"]
        t_key = dna["key_name"]

    lang_opt = st.selectbox("言語構成",
                            ["日本語（サビは英語も混ぜる）", "全日本語", "韓国語（サビは英語も混ぜる）", "全英語"])
    boost_mode = st.toggle("Anthemic Boost", value=True)
    optimizer = st.toggle("Top-Chart Optimizer", value=True)

# =========================
#  Logic & Generation
# =========================
if st.button("⚡ Generate Hit-DNA Production Prompt"):
    # 楽器ロジック復元
    inst_detail = "Modern J-POP production."
    if "Ballad" in genre_key:
        inst_detail = "Grand Piano, emotional strings, delicate live percussion."
    elif "Rock" in genre_key:
        inst_detail = "Overdriven guitars, energetic bass, real acoustic drums."
    elif "City Pop" in genre_key:
        inst_detail = "Fretless bass, funky Rhodes, vintage 80s DX7 synth pads."
    elif "Lo-fi" in genre_key:
        inst_detail = "Chill Rhodes, dusty vinyl crackle, boom-bap drums."
    elif "Vocaloid" in genre_key:
        inst_detail = "Aggressive digital synths, fast piano arpeggios, glitch effects."

    # 作曲プロンプト (空白詰め)
    opt_logic = f"Hit-Logic:Intro<15s,1st Chorus<45s.High loudness,peak energy at chorus." if optimizer else ""
    style_raw = (
        f"Genre:{genre_key}.BPM:{t_bpm}.Key:{t_key}.Energy:{dna['energy']}.Inst:{inst_detail}Vocal:{v_gender}.{'Anthemic soaring chorus boost.' if boost_mode else ''}{opt_logic}Avoid:{negative_p if negative_p else 'none'}.").replace(
        "  ", " ").strip()

    # 作詞プロンプト (空白詰め)
    lyrics_raw = (
        f"Professional lyrics for {genre_key}.Language:{lang_opt}.POV:{l_pov}.Theme:{must_have}.Exclude:{negative_p if negative_p else 'none'}.Structure:[Intro][Verse1][Pre-Chorus][Chorus][Verse2][Chorus][Bridge][Chorus][Outro].Guidelines:Emotional imagery,rhythmic alignment with {t_bpm}BPM.").replace(
        "  ", " ").strip()

    # 文字数制限
    style_final = style_raw[:limit]
    lyrics_final = lyrics_raw[:limit]

    # 表示
    st.markdown("### 🧪 生成結果 (DNA-Synced)")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Style / Composition Prompt")
    st.text_area("作曲指示", value=style_final, height=150, key="st_ta")
    st.subheader("✍️ Lyrics Prompt")
    st.text_area("作詞指示", value=lyrics_final, height=220, key="ly_ta")

    all_output = f"【STYLE】\n{style_final}\n\n【LYRICS】\n{lyrics_final}"
    st.download_button("⬇️ プロンプトを保存", data=all_output, file_name="hitforge_production.txt")

    st.subheader("🧠 DNA Analysis")
    st.markdown(
        f"""<div style="margin-top:10px;"><span class="gold-chip">BPM: {t_bpm}</span><span class="gold-chip">KEY: {t_key}</span><span class="gold-chip">ENERGY: {dna['energy']}</span><p style='color:#e3b341; margin-top:10px;'>Logic: {dna['logic']}</p></div>""",
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)