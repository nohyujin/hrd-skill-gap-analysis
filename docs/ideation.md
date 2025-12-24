로컬 환경에서 큰 비용이나 복잡한 서버 구축 없이 바로 실행해 볼 수 있는 **'Python 기반 스킬 갭 분석 MVP'** 프로젝트를 제안합니다. 이 프로젝트는 데이터 분석과 UI를 동시에 잡을 수 있는 **Streamlit** 라이브러리를 활용하는 것이 핵심입니다.

---

## 🛠️ MVP 기술 스택

* **언어:** Python 3.x
* **프레임워크:** **Streamlit** (웹 대시보드를 코드 몇 줄로 만들어주는 라이브러리)
* **데이터 관리:** **Pandas** (Excel/CSV 데이터 핸들링)
* **시각화:** **Plotly** (인터랙티브한 레이더 차트 및 히트맵 생성)
* **저장소:** 로컬 CSV 파일 (별도 DB 설치 불필요)

---

## 📋 프로젝트 구현 단계

### 1단계: 기초 데이터 설계 (Excel/CSV)

먼저 로컬에서 `skills_data.csv` 파일을 만듭니다. 이 파일이 시스템의 DB 역할을 합니다.

| 사원명 | 직무 | 스킬 항목 | 현재 점수 (Actual) | 목표 점수 (Target) |
| --- | --- | --- | --- | --- |
| 김철수 | 데이터 분석가 | Python | 3 | 5 |
| 김철수 | 데이터 분석가 | SQL | 4 | 4 |
| 김철수 | 데이터 분석가 | 통계 | 2 | 4 |
| 이영희 | HRD 담당자 | 기획력 | 4 | 5 |
| 이영희 | HRD 담당자 | 커뮤니케이션 | 5 | 5 |

### 2단계: 핵심 기능 구현 (Python Code)

`app.py`라는 파일을 만들고 다음과 같은 구조로 코드를 작성합니다.

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 데이터 로드
df = pd.read_csv('skills_data.csv')

st.title("🎯 HRD 스킬 갭 분석 대시보드")

# 2. 사용자 선택 (Sidebar)
user_list = df['사원명'].unique()
selected_user = st.sidebar.selectbox("직원을 선택하세요", user_list)

# 3. 데이터 필터링
user_data = df[df['사원명'] == selected_user]

# 4. 시각화 (레이더 차트)
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=user_data['현재 점수 (Actual)'], theta=user_data['스킬 항목'], fill='toself', name='현재 역량'))
fig.add_trace(go.Scatterpolar(r=user_data['목표 점수 (Target)'], theta=user_data['스킬 항목'], name='목표 역량'))

st.plotly_chart(fig)

# 5. 스킬 갭 분석 결과 출력
user_data['Gap'] = user_data['목표 점수 (Target)'] - user_data['현재 점수 (Actual)']
gap_needed = user_data[user_data['Gap'] > 0]

st.subheader(f"🔍 {selected_user}님의 집중 보완 필요 역량")
st.table(gap_needed[['스킬 항목', 'Gap']])

```

### 3단계: 로컬 실행 방법

터미널(또는 CMD)에서 다음 명령어를 입력하면 로컬 웹 브라우저에 즉시 대시보드가 뜹니다.

```bash
pip install streamlit pandas plotly
streamlit run app.py

```

---

## ✨ 이 MVP의 차별화 포인트 (발전 방향)

로컬 MVP 수준에서 다음 기능을 추가하면 실제 HRD 현업에서 바로 쓸 수 있는 수준이 됩니다.

1. **AI 교육 추천 (LLM 연동):**
* `Gap`이 발생한 스킬명을 OpenAI API(ChatGPT)에 던져서 "이 스킬을 보완하기 위한 커리큘럼 3개를 추천해줘"라는 문구를 대시보드 하단에 자동 생성.


2. **부서별 평균 비교:**
* 내 점수뿐만 아니라 '부서 평균 점수'를 레이더 차트에 한 겹 더 씌워 내가 팀 내에서 어느 정도 위치인지 파악.


3. **데이터 업로드 기능:**
* `st.file_uploader`를 사용해 인사 담당자가 엑셀 파일을 업로드하면 즉시 분석 결과가 나오도록 구현.



---

## 💡 HRD 포트폴리오로서의 가치

이 프로젝트를 완성하면 다음과 같은 역량을 증명할 수 있습니다.

* **HR 테크 이해도:** HR 데이터를 단순히 보는 것에 그치지 않고 솔루션화할 수 있음.
* **문제 해결 능력:** 스킬 갭이라는 현업의 문제를 IT 도구로 시각화함.
* **데이터 리터러시:** 데이터를 가공하여 인사이트(보완 필요 역량)를 도출함.

**이 로컬 MVP를 실제로 구현해 보시겠어요? 막히는 코드가 있다면 구체적인 파이썬 로직을 짜드릴 수 있습니다.**