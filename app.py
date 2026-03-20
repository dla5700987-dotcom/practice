import streamlit as st
import pandas as pd
import os

DATA_FILE = "books.csv"

# ---------------------------
# 데이터 로드/저장
# ---------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=[
            "책 이름", "저자", "출판사", "장르", "등장인물", "줄거리", "기타"
        ])

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# 초기 데이터
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

st.set_page_config(layout="wide")

# ── 양피지 질감 배경 CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* 전체 앱 배경 – 양피지 색상 + SVG 노이즈 필터로 질감 구현 */
.stApp {
    background-color: #ffffff;
    font-family: 'Georgia', serif;
}

/* 사이드바 배경 – 기존 유지 */
[data-testid="stSidebar"] {
    background-color: #e8d5a3 !important;
    border-right: 2px solid #c9a96e !important;
}

/* 메인 컨텐츠 영역 */
[data-testid="stMain"] {
    background: transparent !important;
}

/* 텍스트 색상 – 오래된 잉크 느낌 */
h1, h2, h3, h4, h5, h6,
.stTitle, .stSubheader {
    color: #3b2a1a !important;
    font-family: 'Georgia', serif !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.12);
}

p, label, div {
    color: #3b2a1a;
}

/* Expander – 두루마리 카드 느낌 */
[data-testid="stExpander"] {
    background-color: rgba(245, 228, 190, 0.85) !important;
    border: 1px solid #c9a96e !important;
    border-radius: 4px !important;
    box-shadow: 2px 3px 8px rgba(100, 70, 20, 0.18);
}

/* 입력 필드 */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: #fdf6e3 !important;
    border: 1px solid #c9a96e !important;
    color: #3b2a1a !important;
    font-family: 'Georgia', serif !important;
}

/* 버튼 */
.stButton > button {
    background-color: #8b6530 !important;
    color: #fdf6e3 !important;
    border: 1px solid #6b4c24 !important;
    border-radius: 4px !important;
    font-family: 'Georgia', serif !important;
    font-weight: bold;
    transition: background-color 0.2s;
}
.stButton > button:hover {
    background-color: #6b4c24 !important;
}

/* 구분선 */
hr {
    border-color: #c9a96e !important;
}

/* 성공/경고 메시지 */
[data-testid="stAlert"] {
    background-color: rgba(245, 228, 190, 0.9) !important;
    border-color: #c9a96e !important;
    color: #3b2a1a !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 소설 데이터 저장 다이어리")

# ---------------------------
# 사이드바 입력
# ---------------------------
st.sidebar.header("📌 데이터 입력")

with st.sidebar.form("input_form"):
    title = st.text_input("책 이름")
    author = st.text_input("저자")
    publisher = st.text_input("출판사")
    genre = st.text_input("장르")
    characters = st.text_area("등장인물")
    story = st.text_area("줄거리")
    etc = st.text_area("기타")

    submitted = st.form_submit_button("저장")

    if submitted:
        new_data = pd.DataFrame([{
            "책 이름": title,
            "저자": author,
            "출판사": publisher,
            "장르": genre,
            "등장인물": characters,
            "줄거리": story,
            "기타": etc
        }])

        st.session_state.df = pd.concat([df, new_data], ignore_index=True)
        save_data(st.session_state.df)
        st.success("저장 완료!")

# ---------------------------
# CSV 업로드
# ---------------------------
st.sidebar.header("📂 CSV 업로드")
uploaded_file = st.sidebar.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    upload_df = pd.read_csv(uploaded_file)
    st.session_state.df = pd.concat([st.session_state.df, upload_df], ignore_index=True)
    save_data(st.session_state.df)
    st.sidebar.success("CSV 업로드 완료!")

# ---------------------------
# 검색
# ---------------------------
st.sidebar.header("🔍 검색")
keyword = st.sidebar.text_input("검색어 입력")

if keyword:
    filtered_df = st.session_state.df[
        st.session_state.df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
    ]
else:
    filtered_df = st.session_state.df

# ---------------------------
# 메인 화면
# ---------------------------
st.subheader("📊 저장된 데이터")

if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        title_display = f"✍️ {row['저자']} - 📖 {row['책 이름']}"

        with st.expander(title_display):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**책 이름:** {row['책 이름']}")
                st.write(f"**저자:** {row['저자']}")
                st.write(f"**출판사:** {row['출판사']}")
                st.write(f"**장르:** {row['장르']}")

            with col2:
                st.write(f"**등장인물:** {row['등장인물']}")
                st.write(f"**줄거리:** {row['줄거리']}")
                st.write(f"**기타:** {row['기타']}")

            # 수정 기능
            st.markdown("---")
            st.write("✏️ 수정")

            new_title = st.text_input("책 이름", row["책 이름"], key=f"title_{idx}")
            new_author = st.text_input("저자", row["저자"], key=f"author_{idx}")
            new_publisher = st.text_input("출판사", row["출판사"], key=f"publisher_{idx}")
            new_genre = st.text_input("장르", row["장르"], key=f"genre_{idx}")
            new_characters = st.text_area("등장인물", row["등장인물"], key=f"char_{idx}")
            new_story = st.text_area("줄거리", row["줄거리"], key=f"story_{idx}")
            new_etc = st.text_area("기타", row["기타"], key=f"etc_{idx}")

            if st.button("💾 수정 저장", key=f"save_{idx}"):
                st.session_state.df.loc[idx] = [
                    new_title, new_author, new_publisher,
                    new_genre, new_characters, new_story, new_etc
                ]
                save_data(st.session_state.df)
                st.success("수정 완료!")

            # 삭제 기능
            if st.button("🗑️ 삭제", key=f"delete_{idx}"):
                st.session_state.df = st.session_state.df.drop(idx).reset_index(drop=True)
                save_data(st.session_state.df)
                st.warning("삭제 완료! 새로고침 해주세요.")
else:
    st.info("데이터가 없습니다.")
