import streamlit as st
import pandas as pd

st.set_page_config(page_title="비캔버스 변환기", layout="wide")

st.title("👕 색상 + 사이즈 변환 v1.1")
st.write("약 1400개의 비캔버스 반팔티를 색상과 사이즈로 변환하여 검색할 수 있습니다.")
st.write("규칙 : 비캔버스 전색상 (이름) 피그먼트 반팔티, 색상, 사이즈, 수량")

# CSV 로드
df = pd.read_csv("be_canvas.csv", header=None)
df = df.astype(str).apply(lambda col: col.str.strip())

col1, col2 = st.columns(2)
with col1:
    new_color = st.text_input("변경할 색상", placeholder="예: 피그먼트브라운")
with col2:
    new_size = st.text_input("변경할 사이즈", placeholder="예: L")

# 변환 실행
if st.button("변환하기"):
    if new_color and new_size:

        if df.shape[1] >= 4:
            df_copy = df.copy()

            df_copy[1] = new_color
            df_copy[2] = new_size

            # 문장 리스트 생성
            result_lines = df_copy.apply(
                lambda row: ", ".join([str(x).strip() for x in row[:4]]),
                axis=1
            ).tolist()

            # 세션에 저장 (검색용)
            st.session_state["result_lines"] = result_lines

        else:
            st.error("❌ CSV 구조 오류")
    else:
        st.warning("⚠️ 색상/사이즈 입력 필요")

# 변환 결과가 있을 때만 검색 가능
if "result_lines" in st.session_state:

    st.subheader("🔍 변환 결과 검색")

    search_keyword = st.text_input("변환된 결과에서 검색", placeholder="예: 쇼핑")

    result_lines = st.session_state["result_lines"]

    # 검색 필터
    if search_keyword:
        filtered = [line for line in result_lines if search_keyword in line]
    else:
        filtered = result_lines

    # 결과 출력
    output_text = "\n".join(filtered)

    st.text_area("📋 복사용 결과", output_text, height=300)

    # 검색 결과 없을 때
    if search_keyword and not filtered:
        st.warning("❌ 검색 결과 없음")

    st.download_button(
        label="TXT 다운로드",
        data=output_text,
        file_name="result.txt",
        mime="text/plain"
    )

st.write("업데이트 내역 : \n- v1.0 : 초기 버전 출시 \n- v1.1 : txt 파일 다운로드 후 띄어쓰기 개선 + 6개의 반팔티 추가")
