import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="독버섯 데이터 저장소", layout="wide")

st.title("🍄 독버섯 데이터 관리 앱")

DATA_FILE = "mushroom_data.csv"

# 파일이 없으면 초기 생성
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["자생지", "버섯 이름", "독성 유무", "섭취시 증상"])
    df_init.to_csv(DATA_FILE, index=False)

# 데이터 불러오기
df = pd.read_csv(DATA_FILE)

# -------------------------
# 입력 폼
# -------------------------
st.subheader("📌 데이터 입력")

with st.form("input_form"):
    habitat = st.text_input("자생지 (예: 북한산 침엽수림)")
    name = st.text_input("버섯 이름")
    toxicity = st.selectbox("독성 유무", ["독 있음", "독 없음", "불명"])
    symptoms = st.text_area("섭취 시 증상")

    submitted = st.form_submit_button("저장")

    if submitted:
        new_data = pd.DataFrame({
            "자생지": [habitat],
            "버섯 이름": [name],
            "독성 유무": [toxicity],
            "섭취시 증상": [symptoms]
        })

        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success("데이터가 저장되었습니다.")

# -------------------------
# 데이터 보기
# -------------------------
st.subheader("📊 저장된 데이터")

df = pd.read_csv(DATA_FILE)
st.dataframe(df, use_container_width=True)

# -------------------------
# 간단 검색 기능
# -------------------------
st.subheader("🔍 검색")

search_name = st.text_input("버섯 이름 검색")

if search_name:
    filtered = df[df["버섯 이름"].str.contains(search_name, case=False, na=False)]
    st.dataframe(filtered, use_container_width=True)
