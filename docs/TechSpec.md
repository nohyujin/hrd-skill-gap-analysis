# Technical Specification
# HRD 스킬 갭 분석 대시보드

**버전:** 1.0  
**작성일:** 2025-12-24  
**작성자:** nohyujin

---

## 📋 Table of Contents

1. [개요](#개요)
2. [기술 스택](#기술-스택)
3. [시스템 아키텍처](#시스템-아키텍처)
4. [데이터 모델](#데이터-모델)
5. [컴포넌트 설계](#컴포넌트-설계)
6. [UI/UX 설계](#uiux-설계)
7. [성능 요구사항](#성능-요구사항)
8. [보안 고려사항](#보안-고려사항)
9. [배포 전략](#배포-전략)
10. [향후 확장성](#향후-확장성)

---

## 개요

### 프로젝트 목적
HR 담당자와 직원들이 스킬 갭을 시각적으로 분석하고 데이터 기반 교육 계획을 수립할 수 있는 웹 기반 대시보드 구축

### 기술적 목표
- **단순성**: 복잡한 인프라 없이 로컬 환경에서 즉시 실행 가능
- **확장성**: 향후 클라우드 배포 및 기능 확장 가능한 구조
- **성능**: 100명 이상의 데이터에서도 5초 이내 로딩
- **유지보수성**: 명확한 코드 구조와 문서화

---

## 기술 스택

### Core Technologies

#### 1. Python 3.x
**버전:** 3.7 이상 (권장: 3.9+)

**선택 이유:**
- 데이터 분석에 최적화된 언어
- 풍부한 라이브러리 생태계
- Streamlit과의 완벽한 통합

**사용 영역:**
- 백엔드 로직
- 데이터 처리 및 분석
- API 연동 (향후)

---

#### 2. Streamlit
**버전:** 1.28.0 이상

**선택 이유:**
- 빠른 프로토타이핑 가능
- Python 코드만으로 웹 UI 구현
- 자동 리렌더링 및 상태 관리
- 별도의 프론트엔드 개발 불필요

**주요 기능 활용:**
- `st.sidebar`: 사이드바 UI
- `st.selectbox`: 드롭다운 메뉴
- `st.plotly_chart`: 차트 렌더링
- `st.table`: 데이터 테이블 표시
- `st.file_uploader`: 파일 업로드 (Phase 5)
- `st.cache_data`: 데이터 캐싱

**설정:**
```python
st.set_page_config(
    page_title="HRD 스킬 갭 분석",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

---

#### 3. Pandas
**버전:** 2.0.0 이상

**선택 이유:**
- CSV/Excel 데이터 핸들링의 표준
- 강력한 데이터 조작 기능
- Streamlit과의 원활한 통합

**주요 기능 활용:**
- `pd.read_csv()`: CSV 파일 읽기
- `pd.read_excel()`: Excel 파일 읽기 (Phase 5)
- `DataFrame.groupby()`: 부서별 평균 계산 (Phase 5)
- `DataFrame.filter()`: 데이터 필터링
- `DataFrame.sort_values()`: 정렬

**데이터 처리 예시:**
```python
# CSV 로드
df = pd.read_csv('skills_data.csv', encoding='utf-8')

# 직원별 필터링
user_data = df[df['사원명'] == selected_user]

# 갭 계산
user_data['Gap'] = user_data['목표 점수 (Target)'] - user_data['현재 점수 (Actual)']

# 보완 필요 스킬 필터링
gap_needed = user_data[user_data['Gap'] > 0].sort_values('Gap', ascending=False)
```

---

#### 4. Plotly
**버전:** 5.17.0 이상

**선택 이유:**
- 인터랙티브한 시각화
- 레이더 차트 지원
- 반응형 디자인
- 마우스 오버 시 상세 정보 표시

**주요 기능 활용:**
- `go.Scatterpolar`: 레이더 차트
- `go.Figure`: 차트 객체 생성
- `update_layout()`: 차트 레이아웃 커스터마이징

**레이더 차트 구현:**
```python
import plotly.graph_objects as go

fig = go.Figure()

# 현재 역량
fig.add_trace(go.Scatterpolar(
    r=user_data['현재 점수 (Actual)'],
    theta=user_data['스킬 항목'],
    fill='toself',
    name='현재 역량',
    fillcolor='rgba(0, 123, 255, 0.3)',
    line=dict(color='rgb(0, 123, 255)', width=2)
))

# 목표 역량
fig.add_trace(go.Scatterpolar(
    r=user_data['목표 점수 (Target)'],
    theta=user_data['스킬 항목'],
    name='목표 역량',
    line=dict(color='rgb(255, 99, 71)', width=2, dash='dash')
))

# 레이아웃 설정
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5],
            tickmode='linear',
            tick0=0,
            dtick=1
        )
    ),
    showlegend=True,
    title="스킬 역량 분석",
    height=500
)
```

---

### Development Tools

#### 5. Git & GitHub
**버전:** Git 2.x, GitHub CLI 2.x

**사용 목적:**
- 버전 관리
- 협업 및 코드 리뷰
- 이슈 트래킹
- CI/CD (향후)

---

#### 6. Virtual Environment
**도구:** venv (Python 내장)

**설정:**
```bash
# 가상환경 생성
python -m venv venv

# 활성화 (Windows)
venv\Scripts\activate

# 활성화 (Mac/Linux)
source venv/bin/activate
```

---

### Optional Dependencies (Phase 5)

#### 7. OpenAI API
**버전:** openai 1.0.0 이상

**사용 목적:** AI 기반 교육 추천

**구현 예시:**
```python
import openai

def get_training_recommendations(skill_name, gap_score):
    prompt = f"""
    스킬: {skill_name}
    현재 부족한 정도: {gap_score}점
    
    이 스킬을 보완하기 위한 구체적인 교육 커리큘럼 3개를 추천해주세요.
    각 추천은 다음 형식으로 작성해주세요:
    1. 과정명
    2. 학습 기간
    3. 핵심 내용
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content
```

---

## 시스템 아키텍처

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                         │
│                  (http://localhost:8501)                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ HTTP
                      │
┌─────────────────────▼───────────────────────────────────┐
│                Streamlit Server                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              app.py (Main App)                  │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │         UI Components                    │  │   │
│  │  │  - Sidebar (직원 선택)                   │  │   │
│  │  │  - Radar Chart (레이더 차트)             │  │   │
│  │  │  - Gap Table (갭 분석 테이블)            │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────┐  │   │
│  │  │      Business Logic Layer                │  │   │
│  │  │  - load_data()                           │  │   │
│  │  │  - filter_user_data()                    │  │   │
│  │  │  - calculate_gap()                       │  │   │
│  │  │  - create_radar_chart()                  │  │   │
│  │  └──────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────┘
                      │
                      │ File I/O
                      │
┌─────────────────────▼───────────────────────────────────┐
│                 Data Layer                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │           skills_data.csv                        │  │
│  │  (사원명, 직무, 스킬 항목, 현재 점수, 목표 점수) │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
User Action (직원 선택)
    ↓
Streamlit Event Handler
    ↓
filter_user_data(selected_user)
    ↓
calculate_gap(user_data)
    ↓
create_radar_chart(user_data) + create_gap_table(gap_data)
    ↓
Streamlit Re-render
    ↓
Updated UI Display
```

---

## 데이터 모델

### CSV Schema (MVP)

#### skills_data.csv

| 필드명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| 사원명 | String | NOT NULL | 직원 이름 (고유하지 않음) |
| 직무 | String | NOT NULL | 직무/직책 |
| 스킬 항목 | String | NOT NULL | 평가 대상 스킬명 |
| 현재 점수 (Actual) | Integer | 1-5 | 현재 역량 수준 |
| 목표 점수 (Target) | Integer | 1-5 | 목표 역량 수준 |

**예시 데이터:**
```csv
사원명,직무,스킬 항목,현재 점수 (Actual),목표 점수 (Target)
김철수,데이터 분석가,Python,3,5
김철수,데이터 분석가,SQL,4,4
김철수,데이터 분석가,통계,2,4
이영희,HRD 담당자,기획력,4,5
이영희,HRD 담당자,커뮤니케이션,5,5
```

**데이터 무결성 규칙:**
- 점수는 1-5 범위 내에 있어야 함
- 모든 필드는 필수값
- UTF-8 인코딩 사용

---

### Extended Schema (Phase 5)

#### skills_data_extended.csv

| 필드명 | 데이터 타입 | 제약 조건 | 설명 |
|--------|------------|-----------|------|
| 사원명 | String | NOT NULL | 직원 이름 |
| 직무 | String | NOT NULL | 직무/직책 |
| **부서** | String | NOT NULL | 소속 부서 (Phase 5 추가) |
| 스킬 항목 | String | NOT NULL | 평가 대상 스킬명 |
| **스킬 카테고리** | String | NULLABLE | 스킬 분류 (Phase 5 추가) |
| 현재 점수 (Actual) | Integer | 1-5 | 현재 역량 수준 |
| 목표 점수 (Target) | Integer | 1-5 | 목표 역량 수준 |
| **평가일** | Date | NULLABLE | 평가 날짜 (Phase 5 추가) |

---

### In-Memory Data Structure

```python
# Pandas DataFrame 구조
df = pd.DataFrame({
    '사원명': ['김철수', '김철수', '이영희'],
    '직무': ['데이터 분석가', '데이터 분석가', 'HRD 담당자'],
    '스킬 항목': ['Python', 'SQL', '기획력'],
    '현재 점수 (Actual)': [3, 4, 4],
    '목표 점수 (Target)': [5, 4, 5]
})

# 계산된 필드 추가
df['Gap'] = df['목표 점수 (Target)'] - df['현재 점수 (Actual)']
```

---

## 컴포넌트 설계

### 1. Data Loading Module

**파일:** `app.py` (또는 분리 시 `data_loader.py`)

**함수:**
```python
@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    CSV 파일을 로드하고 검증합니다.
    
    Args:
        file_path: CSV 파일 경로
        
    Returns:
        pd.DataFrame: 로드된 데이터프레임
        
    Raises:
        FileNotFoundError: 파일이 존재하지 않을 때
        ValueError: 데이터 형식이 올바르지 않을 때
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        validate_data(df)
        return df
    except FileNotFoundError:
        st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        st.stop()
    except Exception as e:
        st.error(f"❌ 데이터 로드 중 오류 발생: {str(e)}")
        st.stop()

def validate_data(df: pd.DataFrame) -> None:
    """
    데이터프레임의 유효성을 검증합니다.
    
    Args:
        df: 검증할 데이터프레임
        
    Raises:
        ValueError: 필수 컬럼이 없거나 데이터가 유효하지 않을 때
    """
    required_columns = ['사원명', '직무', '스킬 항목', '현재 점수 (Actual)', '목표 점수 (Target)']
    
    # 필수 컬럼 확인
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(f"필수 컬럼이 없습니다: {missing_columns}")
    
    # 점수 범위 확인
    if not df['현재 점수 (Actual)'].between(1, 5).all():
        raise ValueError("현재 점수는 1-5 범위여야 합니다.")
    
    if not df['목표 점수 (Target)'].between(1, 5).all():
        raise ValueError("목표 점수는 1-5 범위여야 합니다.")
    
    # 빈 값 확인
    if df[required_columns].isnull().any().any():
        raise ValueError("필수 필드에 빈 값이 있습니다.")
```

---

### 2. Data Processing Module

**함수:**
```python
def filter_user_data(df: pd.DataFrame, user_name: str) -> pd.DataFrame:
    """
    특정 사용자의 데이터를 필터링합니다.
    
    Args:
        df: 전체 데이터프레임
        user_name: 필터링할 사용자 이름
        
    Returns:
        pd.DataFrame: 필터링된 데이터프레임
    """
    return df[df['사원명'] == user_name].copy()

def calculate_gap(df: pd.DataFrame) -> pd.DataFrame:
    """
    스킬 갭을 계산합니다.
    
    Args:
        df: 사용자 데이터프레임
        
    Returns:
        pd.DataFrame: 갭이 추가된 데이터프레임
    """
    df['Gap'] = df['목표 점수 (Target)'] - df['현재 점수 (Actual)']
    return df

def get_gap_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    보완이 필요한 스킬을 추출하고 정렬합니다.
    
    Args:
        df: 갭이 계산된 데이터프레임
        
    Returns:
        pd.DataFrame: 갭이 있는 스킬만 포함, 갭 크기 순 정렬
    """
    gap_needed = df[df['Gap'] > 0].copy()
    return gap_needed.sort_values('Gap', ascending=False)
```

---

### 3. Visualization Module

**함수:**
```python
def create_radar_chart(df: pd.DataFrame, user_name: str) -> go.Figure:
    """
    레이더 차트를 생성합니다.
    
    Args:
        df: 사용자 데이터프레임
        user_name: 사용자 이름 (타이틀용)
        
    Returns:
        go.Figure: Plotly Figure 객체
    """
    fig = go.Figure()
    
    # 현재 역량
    fig.add_trace(go.Scatterpolar(
        r=df['현재 점수 (Actual)'],
        theta=df['스킬 항목'],
        fill='toself',
        name='현재 역량',
        fillcolor='rgba(0, 123, 255, 0.3)',
        line=dict(color='rgb(0, 123, 255)', width=2)
    ))
    
    # 목표 역량
    fig.add_trace(go.Scatterpolar(
        r=df['목표 점수 (Target)'],
        theta=df['스킬 항목'],
        name='목표 역량',
        line=dict(color='rgb(255, 99, 71)', width=2, dash='dash')
    ))
    
    # 레이아웃
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickmode='linear',
                tick0=0,
                dtick=1,
                showline=True,
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                gridcolor='lightgray'
            )
        ),
        showlegend=True,
        title=dict(
            text=f"{user_name}님의 스킬 역량 분석",
            font=dict(size=20)
        ),
        height=500,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig

def display_gap_table(gap_df: pd.DataFrame, user_name: str) -> None:
    """
    스킬 갭 분석 테이블을 표시합니다.
    
    Args:
        gap_df: 갭 분석 데이터프레임
        user_name: 사용자 이름
    """
    st.subheader(f"🔍 {user_name}님의 집중 보완 필요 역량")
    
    if gap_df.empty:
        st.success("✅ 모든 스킬이 목표 수준에 도달했습니다!")
    else:
        # 표시할 컬럼 선택
        display_df = gap_df[['스킬 항목', '현재 점수 (Actual)', '목표 점수 (Target)', 'Gap']].copy()
        display_df.columns = ['스킬', '현재', '목표', '갭']
        
        # 스타일링
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # 요약 통계
        total_gap = gap_df['Gap'].sum()
        avg_gap = gap_df['Gap'].mean()
        st.caption(f"총 갭: {total_gap}점 | 평균 갭: {avg_gap:.2f}점")
```

---

### 4. Main Application Structure

**파일:** `app.py`

```python
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

# 메인 타이틀
st.title("🎯 HRD 스킬 갭 분석 대시보드")
st.markdown("---")

# 데이터 로드
@st.cache_data
def load_data(file_path='skills_data.csv'):
    # ... (위에서 정의한 함수)
    pass

# 데이터 로드
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터 로드 실패: {e}")
    st.stop()

# 사이드바: 직원 선택
st.sidebar.header("⚙️ 설정")
user_list = sorted(df['사원명'].unique())
selected_user = st.sidebar.selectbox(
    "📋 직원을 선택하세요",
    user_list,
    index=0
)

# 선택된 직원 정보 표시
st.sidebar.markdown("---")
st.sidebar.info(f"**선택된 직원:** {selected_user}")

# 데이터 필터링
user_data = filter_user_data(df, selected_user)
user_data = calculate_gap(user_data)

# 직무 정보 표시
job_role = user_data['직무'].iloc[0]
st.info(f"**직무:** {job_role}")

# 레이아웃: 2열
col1, col2 = st.columns([2, 1])

with col1:
    # 레이더 차트
    st.subheader("📊 스킬 역량 분석")
    fig = create_radar_chart(user_data, selected_user)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # 갭 분석 테이블
    gap_analysis = get_gap_analysis(user_data)
    display_gap_table(gap_analysis, selected_user)

# 푸터
st.markdown("---")
st.caption("💡 HRD Skill Gap Analysis Dashboard v1.0")
```

---

## UI/UX 설계

### Color Scheme

```python
COLORS = {
    'primary': '#007BFF',      # 파란색 (현재 역량)
    'secondary': '#FF6347',    # 빨간색 (목표 역량)
    'success': '#28A745',      # 초록색 (부서 평균, Phase 5)
    'warning': '#FFC107',      # 노란색 (경고)
    'danger': '#DC3545',       # 빨간색 (에러)
    'info': '#17A2B8',         # 청록색 (정보)
    'light': '#F8F9FA',        # 밝은 회색 (배경)
    'dark': '#343A40'          # 어두운 회색 (텍스트)
}
```

### Typography

- **타이틀:** 20px, Bold
- **서브타이틀:** 16px, Semi-bold
- **본문:** 14px, Regular
- **캡션:** 12px, Light

### Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  🎯 HRD 스킬 갭 분석 대시보드                           │
├──────────┬──────────────────────────────────────────────┤
│          │                                              │
│ Sidebar  │         Main Content Area                    │
│          │  ┌────────────────┬──────────────────────┐   │
│ ⚙️ 설정  │  │                │                      │   │
│          │  │  Radar Chart   │   Gap Analysis       │   │
│ 직원선택 │  │                │   Table              │   │
│          │  │                │                      │   │
│          │  └────────────────┴──────────────────────┘   │
│          │                                              │
└──────────┴──────────────────────────────────────────────┘
```

### Responsive Design

- **Wide Layout:** 1200px 이상 - 2열 레이아웃
- **Medium Layout:** 768px-1199px - 1열 레이아웃
- **Mobile:** 767px 이하 - 스택형 레이아웃

---

## 성능 요구사항

### 로딩 성능

| 메트릭 | 목표 | 측정 방법 |
|--------|------|-----------|
| 초기 로딩 시간 | < 5초 | 앱 시작부터 첫 화면 표시까지 |
| 직원 선택 응답 시간 | < 1초 | 드롭다운 선택부터 차트 업데이트까지 |
| 차트 렌더링 시간 | < 500ms | Plotly 차트 생성 및 표시 |

### 데이터 처리 성능

| 데이터 크기 | 처리 시간 | 메모리 사용량 |
|-------------|-----------|---------------|
| 10명, 50개 스킬 | < 1초 | < 50MB |
| 100명, 500개 스킬 | < 3초 | < 200MB |
| 1000명, 5000개 스킬 | < 10초 | < 500MB |

### 최적화 전략

#### 1. 데이터 캐싱
```python
@st.cache_data(ttl=3600)  # 1시간 캐시
def load_data(file_path):
    return pd.read_csv(file_path)
```

#### 2. 계산 최적화
```python
# 벡터화 연산 사용
df['Gap'] = df['목표 점수 (Target)'] - df['현재 점수 (Actual)']

# 루프 대신 pandas 메서드 사용
gap_needed = df[df['Gap'] > 0]  # 빠름
# vs
# gap_needed = [row for row in df if row['Gap'] > 0]  # 느림
```

#### 3. 차트 최적화
```python
# 데이터 포인트 제한
if len(user_data) > 20:
    st.warning("스킬 항목이 많아 상위 20개만 표시합니다.")
    user_data = user_data.nlargest(20, 'Gap')
```

---

## 보안 고려사항

### 데이터 보안

#### 1. 로컬 데이터 보호
- CSV 파일은 `.gitignore`에 추가 (실제 데이터 유출 방지)
- 샘플 데이터만 리포지토리에 포함

```gitignore
# .gitignore
skills_data.csv
*.csv
!sample_data.csv
```

#### 2. 입력 검증
```python
def validate_data(df):
    # SQL Injection 방지 (CSV이므로 직접적 위험은 낮음)
    # XSS 방지 (Streamlit이 자동 이스케이프)
    
    # 데이터 타입 검증
    assert df['현재 점수 (Actual)'].dtype in [int, float]
    assert df['목표 점수 (Target)'].dtype in [int, float]
    
    # 범위 검증
    assert df['현재 점수 (Actual)'].between(1, 5).all()
    assert df['목표 점수 (Target)'].between(1, 5).all()
```

#### 3. API 키 관리 (Phase 5)
```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    st.error("OpenAI API 키가 설정되지 않았습니다.")
    st.stop()
```

**.env 파일:**
```
OPENAI_API_KEY=sk-...
```

**.gitignore에 추가:**
```
.env
```

---

## 배포 전략

### Phase 1: 로컬 개발
```bash
# 개발 환경
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Phase 2: GitHub Actions CI/CD

본 프로젝트는 **GitHub Actions**를 사용하여 자동 빌드 및 배포를 수행합니다.

#### 2.1 GitHub Actions 워크플로우

**.github/workflows/deploy.yml**
```yaml
name: Build and Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest black flake8
      
      - name: Run linting
        run: |
          black --check app.py
          flake8 app.py --max-line-length=100
      
      - name: Run tests
        run: |
          pytest tests/ -v
      
      - name: Build Stlite app
        run: |
          python scripts/build_stlite.py
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

#### 2.2 빌드 프로세스

1. **코드 체크아웃**: 최신 코드 가져오기
2. **Python 환경 설정**: Python 3.9 설치
3. **의존성 설치**: requirements.txt 기반 패키지 설치
4. **코드 품질 검사**: Black, Flake8 실행
5. **테스트 실행**: pytest로 단위 테스트 실행
6. **Stlite 빌드**: Streamlit 앱을 WebAssembly로 변환
7. **아티팩트 업로드**: 빌드 결과물 업로드
8. **GitHub Pages 배포**: 자동 배포

---

### Phase 3: GitHub Pages 배포

#### 3.1 Stlite (WebAssembly) 사용

**Stlite**는 Streamlit을 브라우저에서 실행할 수 있도록 WebAssembly로 변환하는 도구입니다.

**장점:**
- ✅ 서버 불필요 (완전한 클라이언트 사이드 실행)
- ✅ GitHub Pages 무료 호스팅 가능
- ✅ 빠른 로딩 및 응답
- ✅ 무제한 사용자 지원

**단점:**
- ❌ 일부 Python 라이브러리 제한
- ❌ 파일 업로드 기능 제한적
- ❌ 초기 로딩 시간 증가 (WebAssembly 로드)

#### 3.2 Stlite 빌드 스크립트

**scripts/build_stlite.py**
```python
"""
Streamlit 앱을 Stlite (WebAssembly)로 변환하는 빌드 스크립트
"""
import os
import shutil
from pathlib import Path

def build_stlite():
    """Stlite 앱 빌드"""
    
    # 출력 디렉토리 생성
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()
    
    # index.html 생성
    html_content = """
<!DOCTYPE html>
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
</html>
    """
    
    # index.html 저장
    with open(dist_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_content.strip())
    
    print("✅ Stlite 빌드 완료: dist/index.html")

if __name__ == '__main__':
    build_stlite()
```

#### 3.3 GitHub Pages 설정

1. **리포지토리 설정**
   - Settings → Pages
   - Source: GitHub Actions 선택

2. **자동 배포**
   - `main` 브랜치에 푸시 시 자동 빌드 및 배포
   - 배포 URL: `https://nohyujin.github.io/hrd-skill-gap-analysis/`

3. **커스텀 도메인** (선택사항)
   - CNAME 파일 추가
   - DNS 설정

---

### Phase 4: 대안 배포 옵션

#### Option A: Streamlit Cloud (권장 - 서버 사이드)

**장점:**
- ✅ 완전한 Streamlit 기능 지원
- ✅ 파일 업로드 등 모든 기능 사용 가능
- ✅ 무료 티어 제공

**배포 방법:**
1. GitHub 리포지토리 연결
2. Streamlit Cloud에서 앱 선택
3. 자동 배포 및 URL 생성

**URL 예시:** `https://hrd-skill-gap-analysis.streamlit.app`

#### Option B: Docker + Cloud Run

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**배포 명령:**
```bash
# Google Cloud Run 배포
gcloud run deploy hrd-skill-gap-analysis \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

---

## 향후 확장성

### Database Migration Path

**현재 (MVP):** CSV 파일
```
skills_data.csv
```

**Phase 6:** SQLite
```python
import sqlite3

conn = sqlite3.connect('skills.db')
df = pd.read_sql_query("SELECT * FROM skills WHERE 사원명 = ?", conn, params=(selected_user,))
```

**Phase 7:** PostgreSQL/MySQL
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:pass@localhost/hrd_db')
df = pd.read_sql_query("SELECT * FROM skills WHERE 사원명 = %s", engine, params=(selected_user,))
```

### API Development Path

**Phase 8:** REST API
```python
# FastAPI 백엔드
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/users/{user_name}/skills")
def get_user_skills(user_name: str):
    # 데이터 조회 로직
    return {"skills": [...]}
```

### Authentication Path

**Phase 9:** 사용자 인증
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    names, usernames, passwords,
    'cookie_name', 'signature_key', cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # 앱 로직
    pass
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

---

## Dependencies

### requirements.txt

```txt
# Core
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0

# Optional (Phase 5)
openai>=1.0.0
python-dotenv>=1.0.0

# Development
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
```

### Package Versions Lock

```bash
# 정확한 버전 고정
pip freeze > requirements-lock.txt
```

---

## Testing Strategy

### Unit Tests
```python
# test_data_processing.py
import pytest
import pandas as pd
from app import calculate_gap, validate_data

def test_calculate_gap():
    df = pd.DataFrame({
        '현재 점수 (Actual)': [3, 4],
        '목표 점수 (Target)': [5, 4]
    })
    result = calculate_gap(df)
    assert result['Gap'].tolist() == [2, 0]

def test_validate_data_valid():
    df = pd.DataFrame({
        '사원명': ['김철수'],
        '직무': ['개발자'],
        '스킬 항목': ['Python'],
        '현재 점수 (Actual)': [3],
        '목표 점수 (Target)': [5]
    })
    # Should not raise
    validate_data(df)

def test_validate_data_invalid_score():
    df = pd.DataFrame({
        '사원명': ['김철수'],
        '직무': ['개발자'],
        '스킬 항목': ['Python'],
        '현재 점수 (Actual)': [6],  # Invalid
        '목표 점수 (Target)': [5]
    })
    with pytest.raises(ValueError):
        validate_data(df)
```

### Integration Tests
```python
# test_integration.py
def test_full_workflow():
    df = load_data('sample_data.csv')
    user_data = filter_user_data(df, '김철수')
    user_data = calculate_gap(user_data)
    gap_analysis = get_gap_analysis(user_data)
    
    assert not gap_analysis.empty
    assert all(gap_analysis['Gap'] > 0)
```

---

## Monitoring & Logging

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 사용 예시
logger.info(f"User selected: {selected_user}")
logger.error(f"Data load failed: {error}")
```

### Performance Monitoring
```python
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"{func.__name__} took {end-start:.2f}s")
        return result
    return wrapper

@measure_time
def load_data(file_path):
    # ...
    pass
```

---

## Appendix

### A. File Structure
```
hrd-skill-gap-analysis/
├── app.py                  # 메인 애플리케이션
├── requirements.txt        # 패키지 의존성
├── .gitignore             # Git 제외 파일
├── README.md              # 프로젝트 설명
├── docs/
│   ├── PRD.md             # 제품 요구사항 명세
│   ├── TechSpec.md        # 기술 명세 (본 문서)
│   └── ideation.md        # 아이디어 문서
├── data/
│   ├── skills_data.csv    # 실제 데이터 (gitignore)
│   └── sample_data.csv    # 샘플 데이터
├── tests/
│   ├── test_data_processing.py
│   └── test_integration.py
└── .streamlit/
    └── config.toml        # Streamlit 설정
```

### B. Configuration Files

**.streamlit/config.toml**
```toml
[theme]
primaryColor = "#007BFF"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F9FA"
textColor = "#343A40"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
```

---

**문서 버전 관리**
- v1.0 (2025-12-24): 초기 Tech Spec 작성
