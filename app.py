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
    background-color: #3b2a1a;
    font-family: 'Georgia', serif;
}

/* 사이드바 배경 – 기존 유지 */
[data-testid="stSidebar"] {
    background-color: #e8d5a3 !important;
    border-right: 2px solid #c9a96e !important;
}

/* 메인 컨텐츠 영역 – 양피지 이미지 배경 */
[data-testid="stMain"] {
    background-image: url("data:image/webp;base64,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") !important;
    background-size: 160% !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
    background-attachment: fixed !important;
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
