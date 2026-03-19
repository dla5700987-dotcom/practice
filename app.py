import streamlit as st

st.set_page_config(page_title="독버섯 위험도 분석기", layout="centered")

st.title("🍄 독버섯 발생 및 중독 위험도 분석기")
st.markdown("서울 산림 환경 데이터를 기반으로 위험도를 예측합니다.")

# 입력값
st.sidebar.header("환경 입력")

temperature = st.sidebar.slider("기온 (°C)", 10.0, 25.0, 16.0)
humidity = st.sidebar.slider("습도 (%)", 40, 100, 80)
forest_type = st.sidebar.selectbox(
    "식생 유형",
    ["침엽수림", "혼합림", "활엽수림"]
)

# 위험도 계산 함수
def calculate_risk(temp, hum, forest):
    score = 0

    # 기온 조건
    if 15 <= temp <= 17:
        score += 2

    # 습도 조건
    if hum >= 83:
        score += 3
    elif hum >= 80:
        score += 2

    # 식생 조건
    if forest == "침엽수림":
        score += 3
    elif forest == "혼합림":
        score += 1

    return score

risk_score = calculate_risk(temperature, humidity, forest_type)

# 결과 출력
st.subheader("📊 분석 결과")

if risk_score >= 7:
    st.error("🚨 매우 위험: 독버섯 발생 및 중독 가능성 높음")
    st.markdown("👉 야생 버섯 채취 절대 금지")
elif risk_score >= 5:
    st.warning("⚠️ 위험: 독버섯 발생 가능성 있음")
    st.markdown("👉 식별 불확실 시 섭취 금지")
elif risk_score >= 3:
    st.info("🔍 보통: 일부 위험 존재")
else:
    st.success("✅ 낮음: 상대적으로 안전")

# 추가 정보
st.markdown("---")
st.markdown("### 📌 주요 위험 조건")
st.markdown("""
- 침엽수림 (소나무, 잣나무)
- 습도 83% 이상
- 기온 15~17°C
""")

st.markdown("### ☠️ 주요 독버섯")
st.markdown("""
- 붉은사슴뿔버섯
- 독우산광대버섯
- 노란다발버섯
""")

st.markdown("---")
st.caption("※ 본 앱은 연구 기반 참고용이며 실제 식별을 대체하지 않습니다.")
