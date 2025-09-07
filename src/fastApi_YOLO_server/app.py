import streamlit as st
import requests
import json
import base64
import pandas as pd

# FastAPI 서버의 /chat 엔드포인트 URL
base_url = "http://172.30.1.44:8080"
chat_api_url = base_url + "/chat"
yolo_api_url = base_url + "/yolo"

############################
# Streamlit
############################

st.title("API 활용 간단 앱")
st.write("FastAPI 서버와 통신하는 간단한 스트림릿 앱입니다.")
st.markdown("---")

# --- 챗봇 섹션 ---
st.header("1. 챗봇 API")
st.write("메시지를 입력하고 서버로부터 응답을 받습니다.")

# 챗 메시지를 받을 입력 박스
chat_message = st.text_input("메시지 입력:", key="chat_input")

# 메시지 보내기 버튼
if st.button("메시지 보내기"):
    if chat_message:
        try:
            response = requests.post(chat_api_url, params={"msg": chat_message})
            response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.
            chat_response = response.json()
            
            # 응답 결과를 화면에 표시합니다.
            st.success("응답 성공!")
            st.write(f"**질문:** {chat_response.get('prevmessge', 'N/A')}")
            st.write(f"**대답:** {chat_response.get('message', 'N/A')}")
        except requests.exceptions.RequestException as e:
            st.error(f"API 요청 오류: {e}")
            st.info("서버가 실행 중인지, URL이 올바른지 확인해주세요.")
    else:
        st.warning("메시지를 입력해주세요.")
# --- 챗봇 섹션 끝 ---

# --- YOLO 예측 섹션 ---
st.header("2. YOLO 예측 API")
st.write("이미지를 업로드하고 서버로부터 YOLO 예측 결과를 받습니다.")

# 이미지 업로드를 위한 파일 업로더
uploaded_file = st.file_uploader("이미지 파일 업로드", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 이미지 정보를 화면에 표시
    st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("YOLO 예측 시작"):        
        # multipart/form-data 형식으로 이미지 파일을 보냅니다.
        files = {"file": uploaded_file}

        with st.spinner('예측 중...'):
            try:
                response = requests.post(yolo_api_url, files=files)
                response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.
                yolo_response = response.json()
                
                # 예측 결과를 화면에 표시합니다.
                st.success("예측 완료!")
                
                st.write("### 예측 결과")

                # 결과 이미지
                if 'resultImage' in yolo_response and yolo_response['resultImage']:
                    image_data = base64.b64decode(yolo_response['resultImage'])
                    st.image(image_data, caption="결과 이미지", use_container_width=True)
                
                df = pd.DataFrame({
                    "예측명": yolo_response.get('name', []),
                    "예측 신뢰도": yolo_response.get('score', [])
                })
                st.dataframe(df, hide_index=True)

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    st.error("감지된 객체가 없습니다. 다른 이미지를 시도해보세요.")
                else:
                    st.error(f"API 요청 오류: {e}")
                    st.info("서버가 실행 중인지, URL이 올바른지 확인해주세요.")
            except Exception as e:
                st.error(f"예기치 않은 오류 발생: {e}")

# --- YOLO 예측 섹션 끝 ---

############################
############################