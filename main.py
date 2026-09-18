import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)


df = load_data()

# 장르가 여러 개라면 첫 번째 장르만 사용
df["genre"] = (
    df["genre"]
    .fillna("알 수 없음")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 제작 국가 결측값 처리
df["nation"] = (
    df["nation"]
    .fillna("알 수 없음")
    .astype(str)
    .str.strip()
)

# 숫자형 데이터로 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
).fillna(0)

df["first_scrn"] = pd.to_numeric(
    df["first_scrn"],
    errors="coerce"
).fillna(0)

df["first_week_audi"] = pd.to_numeric(
    df["first_week_audi"],
    errors="coerce"
).fillna(0)


# --------------------------------------------------
# 그래프 1
# --------------------------------------------------

st.header("그래프 1. 장르별 영화 편수")

genre_count = df["genre"].value_counts().reset_index()
genre_count.columns = ["장르", "영화 편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    margin=dict(t=60, l=20, r=20, b=20)
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph1_explanation"
)


# --------------------------------------------------
# 그래프 2
# --------------------------------------------------

st.divider()

st.header("그래프 2. 장르별 영화 총 관객 트리맵")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=60, l=20, r=20, b=20)
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph2_explanation"
)


# --------------------------------------------------
# 그래프 3
# --------------------------------------------------

st.divider()

st.header("그래프 3. 총 관객 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객",
    yaxis_title="영화 편수",
    margin=dict(t=60, l=20, r=20, b=20)
)

st.plotly_chart(fig3, use_container_width=True)

# 가장 많은 영화가 몰려 있는 구간 계산
bins = pd.cut(
    df["total_audi"],
    bins=20
)

bin_counts = bins.value_counts().sort_index()
most_common_bin = bin_counts.idxmax()

range_start = most_common_bin.left
range_end = most_common_bin.right

# 가장 관객이 많은 영화
max_audi_index = df["total_audi"].idxmax()
max_movie_name = df.loc[max_audi_index, "movieNm"]
max_movie_audi = df.loc[max_audi_index, "total_audi"]

st.markdown(
    f"""
**대부분의 영화가 몰려 있는 구간:**  
총 관객 **{range_start:,.0f}명 ~ {range_end:,.0f}명** 구간에 가장 많은 영화가 몰려 있습니다.

**가장 관객이 많은 영화:**  
**{max_movie_name}**으로, 총 관객은 **{max_movie_audi:,.0f}명**입니다.
"""
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph3_explanation"
)


# --------------------------------------------------
# 그래프 4
# --------------------------------------------------

st.divider()

st.header("그래프 4. 개봉일 스크린수와 총 관객의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    margin=dict(t=60, l=20, r=20, b=20),
    legend_title="장르"
)

st.plotly_chart(fig4, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph4_explanation"
)


# --------------------------------------------------
# 그래프 5
# --------------------------------------------------

st.divider()

st.header("그래프 5. 장르별 총 관객 분포")

# 장르별 영화 편수 계산
genre_counts = df["genre"].value_counts()

# 영화가 10편 이상인 장르만 선택
valid_genres = genre_counts[genre_counts >= 10].index

boxplot_df = df[df["genre"].isin(valid_genres)].copy()

# 장르별 영화 수가 많은 순서로 정렬
genre_order = (
    boxplot_df["genre"]
    .value_counts()
    .sort_values(ascending=False)
    .index
    .tolist()
)

fig5 = px.box(
    boxplot_df,
    x="genre",
    y="total_audi",
    color="genre",
    category_orders={"genre": genre_order},
    points="outliers",
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객"
    },
    hover_name="movieNm"
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객",
    showlegend=False,
    margin=dict(t=60, l=20, r=20, b=20)
)

st.plotly_chart(fig5, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph5_explanation"
)


# --------------------------------------------------
# 그래프 6
# --------------------------------------------------

st.divider()

st.header("그래프 6. 개봉일 스크린수·총 관객·첫 주 관객의 관계")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=55,
    title="개봉일 스크린수와 총 관객의 관계 - 첫 주 관객 버블 크기",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    }
)

fig6.update_traces(
    marker=dict(
        opacity=0.7,
        line=dict(width=1)
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명<br>"
        "첫 주 관객: %{marker.size:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    margin=dict(t=60, l=20, r=20, b=20),
    legend_title="장르"
)

st.plotly_chart(fig6, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph6_explanation"
)


# --------------------------------------------------
# 그래프 7
# --------------------------------------------------

st.divider()

st.header("그래프 7. 제작 국가 → 장르별 영화 편수")

fig7 = px.sunburst(
    df,
    path=["nation", "genre"],
    title="제작 국가에서 장르로 내려가는 영화 편수",
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(t=60, l=20, r=20, b=20)
)

st.plotly_chart(fig7, use_container_width=True)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 입력하세요.",
    placeholder="이 그래프로 알 수 있는 것을 한 문장으로 작성하세요.",
    height=100,
    key="graph7_explanation"
)
