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
st.write("1년치 일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다.")


# ============================================================
# 데이터 불러오기
# ============================================================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 실제 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자로 사용할 열 변환
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

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 "
    "선 그래프로 확인할 수 있습니다."
)

# 영화 목록
movie_list = sorted(
    df["영화명"].dropna().astype(str).unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

# 선택한 영화 데이터
movie_df = df[df["영화명"].astype(str) == selected_movie].copy()

# 날짜순 정렬
movie_df = movie_df.sort_values("날짜")

# 같은 영화가 하루에 여러 순위로 기록될 가능성을 고려하여
# 날짜별 일관객을 합산
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


# 그래프로 알 수 있는 것
st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "이곳에 그래프를 보고 알 수 있는 내용을 한 문장으로 작성하세요."
)


# ============================================================
# 그래프 2. 앞으로 추가할 그래프
# ============================================================

st.divider()
st.header("📊 그래프 2. 추가 예정")

st.write(
    "앞으로 새로운 그래프를 이 구역에 추가하면 됩니다."
)

st.info(
    "여기에 두 번째 그래프와 "
    "'이 그래프로 알 수 있는 것' 문구를 추가하세요."
)


# ============================================================
# 그래프 3. 앞으로 추가할 그래프
# ============================================================

st.divider()
st.header("📊 그래프 3. 추가 예정")

st.write(
    "여기에 세 번째 그래프를 추가할 수 있습니다."
)

st.info(
    "여기에 세 번째 그래프와 "
    "'이 그래프로 알 수 있는 것' 문구를 추가하세요."
)
