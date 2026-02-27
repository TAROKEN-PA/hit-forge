import streamlit as st
import plotly.graph_objects as go

# 1. グラフを作る「道具（関数）」の定義
def display_futuristic_metrics(bpm_value):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = bpm_value,
        title = {'text': "TARGET BPM", 'font': {'color': "#c9a050", 'size': 20}},
        number = {'font': {'color': "#ffffff", 'size': 50}},
        gauge = {
            'axis': {'range': [60, 200], 'tickwidth': 1, 'tickcolor': "#c9a050"},
            'bar': {'color': "#c9a050"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "#333",
            'steps': [
                {'range': [60, 100], 'color': 'rgba(201, 160, 80, 0.1)'},
                {'range': [100, 160], 'color': 'rgba(201, 160, 80, 0.2)'},
                {'range': [160, 200], 'color': 'rgba(201, 160, 80, 0.3)'}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#ffffff"},
        height=400
    )
    return fig

# 2. 実際に画面に表示する命令（ここが抜けてたお！）
st.title("HitForge Data Analysis")

# 本来はプリセットデータのBPMを入れるけど、まずはテストで「148」を表示！
current_bpm = 148

# グラフを表示しろ！という命令
st.plotly_chart(display_futuristic_metrics(current_bpm), use_container_width=True)

st.write("Spotify DNA Analysis: Complete.")