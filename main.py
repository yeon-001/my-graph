import streamlit as st
import pandas as pd

# --------------------------------
# 페이지 설정
# --------------------------------

st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


# --------------------------------
# 데이터 불러오기
# --------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"])

    # 기온 열 숫자로 변환
    for column in ["평균기온", "최저기온", "최고기온"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# --------------------------------
# 연도별 평균기온 계산
# --------------------------------

df["연도"] = df["날짜"].dt.year

yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)

start_year = int(yearly_temp["연도"].min())
end_year = int(yearly_temp["연도"].max())


# --------------------------------
# 제목
# --------------------------------

st.title("🌡️ 서울의 연평균 기온 변화")

st.markdown(
    "서울의 일별 기온 데이터를 이용해 "
    "**연도별 평균기온의 변화**와 "
    "원본 데이터의 **요약통계**를 살펴봅니다."
)

st.divider()


# --------------------------------
# 연평균 기온 그래프
# --------------------------------

st.subheader(
    f"📈 {start_year}년 ~ {end_year}년 연평균 기온"
)

st.line_chart(
    yearly_temp,
    x="연도",
    y="평균기온",
    x_label="연도",
    y_label="평균기온 (℃)",
    height=500
)

st.caption(
    "※ 각 연도의 일별 평균기온을 평균하여 연평균 기온을 계산했습니다."
)


# --------------------------------
# 데이터 기본 정보
# --------------------------------

st.subheader("📊 데이터 기본 정보")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "전체 관측 건수",
        f"{len(df):,}건"
    )

with col2:
    st.metric(
        "분석 시작 연도",
        f"{start_year}년"
    )

with col3:
    st.metric(
        "분석 마지막 연도",
        f"{end_year}년"
    )

with col4:
    st.metric(
        "분석 연도 수",
        f"{len(yearly_temp):,}년"
    )


# --------------------------------
# 기온 요약통계
# 행과 열을 바꾼 형태
# --------------------------------

st.subheader("📋 원본 데이터 기온 요약통계")

st.markdown(
    "원본 일별 기온 데이터의 "
    "**개수, 평균, 표준편차, 최소값, 사분위수, 중앙값, 최대값**입니다."
)

summary = df[
    ["평균기온", "최저기온", "최고기온"]
].describe()

# 통계 항목을 한국어로 변경
summary = summary.rename(
    index={
        "count": "개수",
        "mean": "평균",
        "std": "표준편차",
        "min": "최소값",
        "25%": "25%",
        "50%": "중앙값",
        "75%": "75%",
        "max": "최대값"
    }
)

# 기온 종류를 열로 설정
summary.columns = [
    "평균기온",
    "최저기온",
    "최고기온"
]

summary = summary.round(2)

st.dataframe(
    summary,
    use_container_width=True
)


# --------------------------------
# 지점 요약통계
# --------------------------------

st.subheader("📍 지점 요약통계")

# 지점별 관측 건수
station_counts = df["지점"].value_counts()

# 지점 요약통계
station_summary = pd.DataFrame({
    "항목": [
        "전체 관측 건수",
        "고유 지점 수",
        "가장 많이 기록된 지점",
        "가장 많이 기록된 지점의 관측 건수",
        "가장 적게 기록된 지점",
        "가장 적게 기록된 지점의 관측 건수"
    ],
    "값": [
        f"{df['지점'].count():,}건",
        f"{df['지점'].nunique():,}개",
        str(station_counts.index[0]),
        f"{station_counts.iloc[0]:,}건",
        str(station_counts.index[-1]),
        f"{station_counts.iloc[-1]:,}건"
    ]
})

st.dataframe(
    station_summary,
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# 지점별 관측 건수
# --------------------------------

with st.expander("📍 지점별 관측 건수 보기"):

    station_table = (
        df["지점"]
        .value_counts()
        .reset_index()
    )

    station_table.columns = [
        "지점",
        "관측 건수"
    ]

    st.dataframe(
        station_table,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------
# 연도별 평균기온
# --------------------------------

with st.expander("📅 연도별 평균기온 데이터 보기"):

    display_df = yearly_temp.copy()

    display_df["평균기온"] = display_df[
        "평균기온"
    ].map(
        lambda x: f"{x:.2f} ℃"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------
# 원본 데이터 미리보기
# --------------------------------

with st.expander("🔎 원본 데이터 미리보기"):

    st.dataframe(
        df.drop(columns=["연도"]).head(100),
        use_container_width=True,
        hide_index=True
    )
