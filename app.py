import streamlit as st
import pandas as pd
import os

# 데이터 파일 경로
DATA_FILE = "mushroom_data.csv"

# 데이터 불러오기
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["자생지", "버섯 이름", "독성 유무", "증상"])

# 데이터 저장
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

st.title("🍄 독버섯 데이터 관리 앱")

# 데이터 로드
df = load_data()

# ------------------------
# 입력 폼
# ------------------------
st.header("📌 데이터 입력")

with st.form("input_form"):
    habitat = st.text_input("자생지")
    name = st.text_input("버섯 이름")
    toxicity = st.selectbox("독성 유무", ["독", "식용 가능", "불명"])
    symptom = st.text_area("섭취 시 증상")

    submitted = st.form_submit_button("저장")

    if submitted:
        new_data = pd.DataFrame([{
            "자생지": habitat,
            "버섯 이름": name,
            "독성 유무": toxicity,
            "증상": symptom
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("데이터가 저장되었습니다.")

# ------------------------
# 검색 기능
# ------------------------
st.header("🔍 데이터 검색")

search_keyword = st.text_input("키워드 검색 (이름/자생지/증상)")

if search_keyword:
    filtered_df = df[
        df.apply(lambda row: row.astype(str).str.contains(search_keyword, case=False).any(), axis=1)
    ]
else:
    filtered_df = df

# ------------------------
# 빠른 필터
# ------------------------
st.header("⚡ 빠른 필터")

col1, col2 = st.columns(2)

with col1:
    habitat_filter = st.selectbox("자생지 필터", ["전체"] + list(df["자생지"].dropna().unique()))

with col2:
    toxicity_filter = st.selectbox("독성 필터", ["전체"] + list(df["독성 유무"].dropna().unique()))

filtered_df2 = filtered_df.copy()

if habitat_filter != "전체":
    filtered_df2 = filtered_df2[filtered_df2["자생지"] == habitat_filter]

if toxicity_filter != "전체":
    filtered_df2 = filtered_df2[filtered_df2["독성 유무"] == toxicity_filter]

# ------------------------
# 결과 출력
# ------------------------
st.header("📊 데이터 목록")
st.dataframe(filtered_df2)

# ------------------------
# 데이터 다운로드
# ------------------------
st.download_button(
    label="📥 CSV 다운로드",
    data=filtered_df2.to_csv(index=False).encode("utf-8-sig"),
    file_name="filtered_mushroom_data.csv",
    mime="text/csv"
)
