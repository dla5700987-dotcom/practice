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
        # 저장 후 검색 초기화
        for key in ["search_habitat", "search_name", "search_toxicity", "search_symptom", "search_active"]:
            if key in st.session_state:
                del st.session_state[key]

# ------------------------
# 검색 기능
# ------------------------
st.header("🔍 데이터 검색")

# 검색 활성 상태 초기화
if "search_active" not in st.session_state:
    st.session_state["search_active"] = False

with st.form("search_form"):
    col1, col2 = st.columns(2)

    with col1:
        search_habitat = st.text_input(
            "자생지",
            value=st.session_state.get("search_habitat", ""),
            placeholder="예: 산림, 초원..."
        )
        search_name = st.text_input(
            "버섯 이름",
            value=st.session_state.get("search_name", ""),
            placeholder="예: 광대버섯..."
        )

    with col2:
        search_toxicity = st.text_input(
            "독성 유무",
            value=st.session_state.get("search_toxicity", ""),
            placeholder="예: 독, 식용 가능, 불명..."
        )
        search_symptom = st.text_input(
            "섭취 시 증상",
            value=st.session_state.get("search_symptom", ""),
            placeholder="예: 구토, 복통..."
        )

    btn_col1, btn_col2 = st.columns([1, 1])

    with btn_col1:
        search_submitted = st.form_submit_button("🔍 검색", use_container_width=True)

    with btn_col2:
        search_cancelled = st.form_submit_button("❌ 취소 (전체 보기)", use_container_width=True)

# 검색 버튼 처리
if search_submitted:
    st.session_state["search_habitat"] = search_habitat
    st.session_state["search_name"] = search_name
    st.session_state["search_toxicity"] = search_toxicity
    st.session_state["search_symptom"] = search_symptom
    st.session_state["search_active"] = True

# 취소 버튼 처리: 검색 상태 초기화
if search_cancelled:
    for key in ["search_habitat", "search_name", "search_toxicity", "search_symptom"]:
        st.session_state[key] = ""
    st.session_state["search_active"] = False
    st.rerun()

# ------------------------
# 필터 적용
# ------------------------
if st.session_state.get("search_active"):
    filtered_df = df.copy()

    s_habitat  = st.session_state.get("search_habitat", "").strip()
    s_name     = st.session_state.get("search_name", "").strip()
    s_toxicity = st.session_state.get("search_toxicity", "").strip()
    s_symptom  = st.session_state.get("search_symptom", "").strip()

    if s_habitat:
        filtered_df = filtered_df[
            filtered_df["자생지"].astype(str).str.contains(s_habitat, case=False, na=False)
        ]
    if s_name:
        filtered_df = filtered_df[
            filtered_df["버섯 이름"].astype(str).str.contains(s_name, case=False, na=False)
        ]
    if s_toxicity:
        filtered_df = filtered_df[
            filtered_df["독성 유무"].astype(str).str.contains(s_toxicity, case=False, na=False)
        ]
    if s_symptom:
        filtered_df = filtered_df[
            filtered_df["증상"].astype(str).str.contains(s_symptom, case=False, na=False)
        ]

    # 검색 조건 요약 표시
    conditions = []
    if s_habitat:  conditions.append(f"자생지: **{s_habitat}**")
    if s_name:     conditions.append(f"버섯 이름: **{s_name}**")
    if s_toxicity: conditions.append(f"독성 유무: **{s_toxicity}**")
    if s_symptom:  conditions.append(f"증상: **{s_symptom}**")

    if conditions:
        st.info(f"🔎 검색 조건 — {' / '.join(conditions)}  |  결과: {len(filtered_df)}건")
    else:
        st.warning("검색 조건을 하나 이상 입력해주세요.")
        filtered_df = df

else:
    filtered_df = df
    st.info(f"📋 전체 데이터: {len(filtered_df)}건")

# ------------------------
# 결과 출력
# ------------------------
st.header("📊 데이터 목록")
st.dataframe(filtered_df, use_container_width=True)

# ------------------------
# 데이터 다운로드
# ------------------------
st.download_button(
    label="📥 CSV 다운로드",
    data=filtered_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="filtered_mushroom_data.csv",
    mime="text/csv"
)
