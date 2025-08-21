import streamlit as st

# ----------------------------
# 인트로
st.title("Hello Streamlit")
st.write("스트림릿 사이트")

name = st.text_input("이름을 입력하세요")

if st.button('실행'):
    st.success(f'안녕하세요: {name}님 반갑습니다.')

# ----------------------------
# 텍스트
st.title("스트림릿 제목")
st.header("헤더")
st.subheader("서브헤더")
st.text("일반 텍스트")
st.markdown("**마크다운 지원** :sparkles:")
st.code("print('Hello World')", language="python")

col1, col2 = st.columns(2)
col1.write("왼쪽 컬럼")
col2.write("오른쪽 컬럼")

# ----------------------------
# 토글
with st.expander("펼치기/접기"):
    st.write("숨겨진 내용")

# ----------------------------
# 인풋
name = st.text_input("이름 입력")
agree = st.checkbox("동의합니다")
option = st.radio("좋아하는 색상", ["빨강", "파랑", "초록"])
select = st.selectbox("과목 선택", ["수학", "과학", "영어"])
multi = st.multiselect("취미 선택", ["독서", "운동", "게임"])

# ----------------------------
# 버튼 클릭
if st.button("클릭"):
    st.success("버튼 눌림")

# ----------------------------
# 파일 업로드
uploaded_file = st.file_uploader("파일 업로드", type=["jpg","png","csv"])

# ----------------------------
# 사이드바
with st.sidebar:
    st.header("필터")
    date = st.date_input("날짜")
    cls = st.selectbox("클래스", ["전체","A","B"])

st.title("대시보드")
st.write("사이드바에서 필터를 조정하세요.")

# ----------------------------
# 컬럼
col1, col2, col3 = st.columns([2, 3, 2])  # 비율로 너비 제어
with col1:
    st.subheader("요약 지표")
    st.metric("Accuracy", "93.2%", "+0.7%")
with col2:
    st.subheader("라인 차트")
    st.line_chart({"acc":[0.8,0.85,0.9,0.932]})
with col3:
    st.subheader("세부 옵션")
    st.checkbox("스무딩")

# ----------------------------
# 탭
tab1, tab2, tab3 = st.tabs(["개요", "지표", "로그"])
with tab1:
    st.write("한 눈에 보는 개요")
with tab2:
    st.write("정밀 지표 표/차트")
with tab3:
    st.code("학습 로그 미리보기...")

# ----------------------------
# 확장
with st.expander("전처리 설명 보기"):
    st.markdown("- 이진화 → 자르기 → 패딩 → 28x28 리사이즈")

# ----------------------------
# 컨테이너 & 플레이스홀더
placeholder = st.empty()        # 화면의 빈 자리 확보
with st.container():
    st.write("섹션 시작")
    st.write("여러 컴포넌트를 묶어 관리")
# 동적으로 업데이트
placeholder.metric("현재 단계", "로딩 중...")
# ... 처리 후
placeholder.metric("현재 단계", "완료")

# ----------------------------
# 폼으로 입력 묶기
with st.form("hyperparams"):
    lr = st.number_input("Learning Rate", 0.0001, 1.0, 0.001, format="%.4f")
    epochs = st.slider("Epochs", 1, 200, 30)
    submitted = st.form_submit_button("학습 시작")
if submitted:
    st.success(f"LR={lr}, Epochs={epochs}로 학습 시작!")

# ----------------------------
# 세션 상태로 상호작용 기억
# 초기화
if "counter" not in st.session_state:
    st.session_state.counter = 0

# 버튼 클릭 시 상태값 변경
if st.button("증가"):
    st.session_state.counter += 1
if st.button("감소"):
    st.session_state.counter -= 1

st.write("현재 값:", st.session_state.counter)


