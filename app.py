import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="독버섯 데이터 관리 시스템", layout="wide")

st.title("🍄 독버섯 자생지 및 특성 관리 시스템")
st.sidebar.header("메뉴 선택")

# 데이터 저장 경로 설정
DATA_FILE = "mushroom_data.csv"

# 초기 데이터 로드 함수
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["버섯 이름", "자생지", "독성 유무", "섭취 시 증상"])

if 'df' not in st.session_state:
    st.session_state.df = load_data()

# --- 사이드바: 데이터 입력 창 ---
with st.sidebar.form("input_form"):
    st.subheader("새로운 데이터 입력")
    name = st.text_input("버섯 이름")
    habitat = st.text_input("자생지")
    is_toxic = st.selectbox("독성 유무", ["독성 있음", "식용/독성 없음", "미확인"])
    symptoms = st.text_area("섭취 시 증상")
    
    submit_button = st.form_submit_button("데이터 추가")

    if submit_button:
        new_data = pd.DataFrame([[name, habitat, is_toxic, symptoms]], 
                                columns=st.session_state.df.columns)
        st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
        st.success(f"'{name}' 데이터가 추가되었습니다.")

# --- 메인 화면: 데이터 관리 및 분석 ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 현재 등록된 데이터")
    st.dataframe(st.session_state.df, use_container_width=True)
    
    # CSV 저장 기능
    if st.button("현재 데이터를 파일로 저장하기"):
        st.session_state.df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
        st.info(f"'{DATA_FILE}'로 저장이 완료되었습니다.")

with col2:
    st.subheader("📥 CSV 데이터 불러오기")
    uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type=["csv"])
    if uploaded_file is not None:
        imported_df = pd.read_csv(uploaded_file)
        if st.button("기존 데이터에 합치기"):
            st.session_state.df = pd.concat([st.session_state.df, imported_df], ignore_index=True)
            st.success("데이터 병합 완료!")

# --- 데이터 내보내기 (Download) ---
st.divider()
csv_data = st.session_state.df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
st.download_button(
    label="전체 데이터 CSV로 내보내기",
    data=csv_data,
    file_name='mushroom_database_export.csv',
    mime='text/csv',
)
