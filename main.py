```python
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# 기본 설정
# ============================================================

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 데이터로 변환
    numeric_columns = [
        "순위",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)
    st.stop()


# ============================================================
# 그래프 1. 영화별 날짜에 따른 일관객 변화
# ============================================================

st.header("📈 그래프 1. 영화별 일관객 변화")

movie_list = sorted(
    df["영화명"].dropna().astype(str).unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")

# 날짜별 일관객 합계
movie_daily = (
    movie_df
    .groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# Plotly 선 그래프
fig = px.line(
    movie_daily,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객"
    }
)

# 마우스를 올렸을 때 날짜와 관객수가 표시되도록 설정
fig.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "관객수: %{y:,.0f}명"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 이 그래프로 알 수 있는 것
# 사용자가 직접 작성
# ============================================================

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 여기에 작성하세요.",
    height=100
)


# ============================================================
# 그래프 2
# 앞으로 새로운 그래프를 추가할 공간
# ============================================================

st.divider()

st.header("📊 그래프 2")

# 여기에 두 번째 그래프를 추가하세요.

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 여기에 작성하세요.",
    height=100,
    key="graph2_explanation"
)


# ============================================================
# 그래프 3
# 앞으로 새로운 그래프를 추가할 공간
# ============================================================

st.divider()

st.header("📊 그래프 3")

# 여기에 세 번째 그래프를 추가하세요.

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 여기에 작성하세요.",
    height=100,
    key="graph3_explanation"
)
```
