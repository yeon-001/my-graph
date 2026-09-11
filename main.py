import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ============================================================
# 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 실제 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형으로 변환
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
# 그래프 1. 영화별 일관객 변화
# ============================================================

st.header("📈 그래프 1. 영화별 일관객 변화")

movie_list = sorted(
    df["영화명"].dropna().astype(str).unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[
    df["영화명"].astype(str) == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")

movie_daily = (
    movie_df
    .groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

fig1 = px.line(
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

fig1.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "관객수: %{y:,.0f}명"
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=500
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 여기에 작성하세요.",
    height=100,
    key="graph1_explanation"
)


# ============================================================
# 그래프 2. 기간 동안 일관객 합계가 가장 큰 5편
# ============================================================

st.divider()

st.header("📊 그래프 2. 일관객 합계 상위 5편")

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)["영화명"]
    .tolist()
)

# 상위 5편만 선택
top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

# 날짜와 영화명 기준으로 정렬
top5_df = top5_df.sort_values(
    ["날짜", "영화명"]
)

# 날짜별 영화별 일관객
top5_daily = (
    top5_df
    .groupby(["날짜", "영화명"], as_index=False)["일관객"]
    .sum()
    .sort_values(["날짜", "영화명"])
)

# 그래프 생성
fig2 = px.line(
    top5_daily,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계가 가장 큰 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=
    "영화: %{fullData.name}<br>"
    "날짜: %{x|%Y-%m-%d}<br>"
    "관객수: %{y:,.0f}명"
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    height=600,
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 여기에 작성하세요.",
    height=100,
    key="graph2_explanation"
)


# ============================================================
# 그래프 3. 날짜별 10위권 일관객 합계
# ============================================================

st.divider()

st.header("📉 그래프 3. 날짜별 10위권 일관객 합계")

# 날짜별 10위권 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 3일 찾기
top3_days = (
    daily_total
    .sort_values("일관객", ascending=False)
    .head(3)
    .copy()
)

# 날짜순으로 정렬
top3_days = top3_days.sort_values("날짜")

# 영역 그래프 생성
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    }
)

# 영역 그래프 모양 설정
fig3.update_traces(
    hovertemplate=
    "날짜: %{x|%Y-%m-%d}<br>"
    "10위권 일관객 합계: %{y:,.0f}명"
)

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계(명)",
    height=600
)


# ============================================================
# 가장 큰 3일을 그래프 위에 표시
# ============================================================

for _, row in top3_days.iterrows():

    date = row["날짜"]
    audience = row["일관객"]

    fig3.add_annotation(
        x=date,
        y=audience,
        text=f"{date.strftime('%Y-%m-%d')}<br>{audience:,.0f}명",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-50,
        font=dict(size=13)
    )


st.plotly_chart(
    fig3,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 여기에 작성하세요.",
    height=100,
    key="graph3_explanation"
)
