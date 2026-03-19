import streamlit as st
import pandas as pd
import os

st.title("🍄 독버섯 데이터 관리")

DATA_FILE = "mushroom_data.csv"

# 파일 초기 생성
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["자생지", "버섯 이름", "독성 유무", "섭취시 증상"])
    df_init.to_csv(DATA_FILE, index=False)

# 입력 영역
st.header("데이터 입력")

habitat = st.text_input("자생지")
name = st.text_input("버섯 이름")
toxicity = st.selectbox("독성 유무", ["독 있음", "독 없음", "불명"])
symptoms = st.text_area("섭취 시 증상")

if st.button("저장"):
    if name == "":
        st.warning("버섯 이름은 필수입니다.")
    else:
        new_data = pd.DataFrame({
            "자생지": [habitat],
            "버섯 이름": [name],
            "독성 유무": [toxicity],
            "섭취시 증상": [symptoms]
        })

        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success("저장 완료!")

# 데이터 표시
st.header("저장된 데이터")

df = pd.read_csv(DATA_FILE)
st.dataframe(df)

# 검색
st.header("검색")

search = st.text_input("버섯 이름 검색")

if search:
    result = df[df["버섯 이름"].str.contains(search, na=False)]
    st.dataframe(result)
