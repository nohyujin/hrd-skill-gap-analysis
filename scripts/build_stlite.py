"""
Streamlit 앱을 Stlite (WebAssembly)로 변환하는 빌드 스크립트
"""
import os
import shutil
from pathlib import Path


def build_stlite():
    """Stlite 앱 빌드"""

    # 출력 디렉토리 생성
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # index.html 생성
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>HRD 스킬 갭 분석 대시보드</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎯</text></svg>">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css">
</head>
<body>
    <div id="root"></div>
    <script type="module">
        import { mount } from "https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js";
        
        // app.py 내용을 여기에 임베드
        const appCode = `
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="HRD 스킬 갭 분석",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 샘플 데이터 (임베디드)
SAMPLE_DATA = '''사원명,직무,스킬 항목,현재 점수 (Actual),목표 점수 (Target)
김철수,데이터 분석가,Python,3,5
김철수,데이터 분석가,SQL,4,4
김철수,데이터 분석가,통계,2,4
김철수,데이터 분석가,머신러닝,2,5
이영희,HRD 담당자,기획력,4,5
이영희,HRD 담당자,커뮤니케이션,5,5
이영희,HRD 담당자,데이터 분석,3,4
박민수,개발자,JavaScript,4,5
박민수,개발자,React,3,5
박민수,개발자,Node.js,3,4'''

@st.cache_data
def load_data():
    from io import StringIO
    return pd.read_csv(StringIO(SAMPLE_DATA))

# 메인 앱 로직
st.title("🎯 HRD 스킬 갭 분석 대시보드")
st.markdown("---")

df = load_data()

# 사이드바
st.sidebar.header("⚙️ 설정")
user_list = sorted(df['사원명'].unique())
selected_user = st.sidebar.selectbox("📋 직원을 선택하세요", user_list)

# 데이터 필터링
user_data = df[df['사원명'] == selected_user].copy()
user_data['Gap'] = user_data['목표 점수 (Target)'] - user_data['현재 점수 (Actual)']

# 직무 정보
job_role = user_data['직무'].iloc[0]
st.info(f"**직무:** {job_role}")

# 레이아웃
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 스킬 역량 분석")
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=user_data['현재 점수 (Actual)'],
        theta=user_data['스킬 항목'],
        fill='toself',
        name='현재 역량',
        fillcolor='rgba(0, 123, 255, 0.3)',
        line=dict(color='rgb(0, 123, 255)', width=2)
    ))
    fig.add_trace(go.Scatterpolar(
        r=user_data['목표 점수 (Target)'],
        theta=user_data['스킬 항목'],
        name='목표 역량',
        line=dict(color='rgb(255, 99, 71)', width=2, dash='dash')
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader(f"🔍 {selected_user}님의 보완 필요 역량")
    gap_needed = user_data[user_data['Gap'] > 0].sort_values('Gap', ascending=False)
    
    if gap_needed.empty:
        st.success("✅ 모든 스킬이 목표 수준에 도달했습니다!")
    else:
        display_df = gap_needed[['스킬 항목', '현재 점수 (Actual)', '목표 점수 (Target)', 'Gap']].copy()
        display_df.columns = ['스킬', '현재', '목표', '갭']
        st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("💡 HRD Skill Gap Analysis Dashboard v1.0 | Powered by Stlite")
`;

        mount(
            {
                requirements: ["plotly"],
                entrypoint: "app.py",
                files: {
                    "app.py": appCode
                }
            },
            document.getElementById("root")
        );
    </script>
</body>
</html>"""

    # index.html 저장
    with open(dist_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content.strip())

    print("✅ Stlite 빌드 완료: dist/index.html")


if __name__ == "__main__":
    build_stlite()
