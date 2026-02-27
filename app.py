import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- 1. ページ設定 (全画面表示) ---
st.set_page_config(layout="wide", page_title="HitForge Data Core")

# --- 2. CSS Style (漆黒・ネオン・黄金) ---
st.markdown(
    """
    <style>
      [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
        background-color: #050609 !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace;
      }
      h1, h2, h3 {
        color: #c9a050 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(201, 160, 80, 0.5);
      }
    </style>
    """, unsafe_allow_html=True
)

st.title("🎧 HITFORGE | CYBER-DATA CYTOSCALE")
st.markdown('<div style="height:1px; width:200px; background:#c9a050; margin-bottom:20px;"></div>',
            unsafe_allow_html=True)

# --- 3. プリセットデータ (たろけんぱさんのデータ) ---
genres = ['J-POP', 'City Pop', 'HipHop', 'Rock', 'Lofi']
bpms = [158, 115, 95, 135, 80]
keys = ['C#m', 'AM7', 'Fm', 'Em', 'Gm']
energy = [0.85, 0.65, 0.75, 0.90, 0.30]
danceability = [0.60, 0.80, 0.90, 0.50, 0.40]


# --- 4. グラフ生成用の道具 (道具を先に定義) ---

# A. 円形ゲージ (BPM)
def create_gauge(value, title, max_val):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': "#ffffff", 'size': 14}},
        number={'font': {'color': "#ffffff", 'size': 24}},
        gauge={'axis': {'range': [60, max_val], 'tickcolor': "#c9a050"},
               'bar': {'color': "#c9a050"},
               'bgcolor': "rgba(0,0,0,0)"}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180,
                      margin=dict(l=10, r=10, t=30, b=10))
    return fig


# B. 棒グラフ (Energy / Dance)
def create_bar(x, y, title, color_scale):
    fig = go.Figure(go.Bar(
        x=x, y=y,
        marker=dict(color=y, colorscale=color_scale),
        text=y, textposition='auto',
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#ffffff"),
                      height=180, title=title, margin=dict(l=10, r=10, t=30, b=10))
    return fig


# C. レーダーチャート (多次元比較)
def create_radar(data):
    fig = go.Figure()
    for i, row in data.iterrows():
        fig.add_trace(
            go.Scatterpolar(r=[row['E'], row['D'], row['K'] / 100, row['E']], theta=['E', 'D', 'K', 'E'], fill='toself',
                            name=row['G']))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"),
                      paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#ffffff"), height=300,
                      title="Multi-Genre DNA Structure", margin=dict(l=10, r=10, t=30, b=10))
    return fig


# --- 5. 画面のレイアウト ( st.columns で分割だお！) ---

# 上段: BPMゲージを5個並べる (全ジャンル一斉分析)
st.markdown("### 📊 Real-Time BPM Analysis")
cols_bpm = st.columns(5)
for i in range(5):
    with cols_bpm[i]:
        st.plotly_chart(create_gauge(bpms[i], genres[i], 200), use_container_width=True)

st.markdown('<div style="height:1px; width:100%; background:rgba(201,160,80,0.2); margin:20px 0;"></div>',
            unsafe_allow_html=True)

# 下段: 2列に分ける
col_left, col_right = st.columns([2, 3])

with col_left:
    st.markdown("### 🌀 Structure Comparison")
    # レーダーチャート
    radar_df = pd.DataFrame({'G': genres, 'E': energy, 'D': danceability, 'K': [95, 80, 70, 85, 60]})
    st.plotly_chart(create_radar(radar_df), use_container_width=True)

    # Keyネオン表示 ( st.metric を近未来化)
    cols_key = st.columns(5)
    for i in range(5):
        with cols_key[i]:
            st.markdown(
                f'<div style="text-align:center; color:#c9a050; border:1px solid #333; padding:10px; border-radius:5px;"><div style="font-size:12px; color:#fff;">{genres[i]}</div><div style="font-size:24px; font-weight:bold;">{keys[i]}</div></div>',
                unsafe_allow_html=True)

with col_right:
    st.markdown("### 📈 Heat Distribution")
    # Energy と Danceability の棒グラフ
    st.plotly_chart(create_bar(genres, energy, "ENERGY PROFILE", [[0, '#050609'], [1, '#c9a050']]),
                    use_container_width=True)
    st.plotly_chart(create_bar(genres, danceability, "DANCEABILITY INDEX", [[0, '#050609'], [1, '#ffffff']]),
                    use_container_width=True)