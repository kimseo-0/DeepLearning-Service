from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel # 잘못된 형식의 데이터가 들어오는 경우 서버가 다운 되지 않도록 처리할 수 있게 도와주는 라이브러리
from typing import List
from PIL import Image
import io
from ultralytics import YOLO
import uuid
from datetime import datetime
import base64

############################
# --- Utills ---
############################

def create_unique_imagename(file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex

    file_extension = file.filename.split('.')[-1]

    # 타임스탬프, UUID, 확장자를 결합하여 고유한 파일명을 만듭니다.
    unique_filename = f"{timestamp}_{unique_id}.{file_extension}"
    return unique_filename

############################
############################


############################
# Model
############################

# 모델 준비
model = YOLO("C:\Potenup\DeepLearning-Service\src\\fastApi_YOLO_server\models\yolo11n.pt")

############################
############################


############################
# FAST API
############################

# fast api 준비
app = FastAPI(title="ResNet34")

class YOLOResponse(BaseModel):
    name : list
    score : list
    resultImage : str

class ChatResponse(BaseModel):
    prevmessge : str
    message : str

@app.get("/")
async def text():
    return {"message": "안녕하세요"}

@app.post("/chat", response_model=ChatResponse)
async def chat(msg : str):
    return ChatResponse(prevmessge = msg, message = "안녕하세요")

# 예측 Api
@app.post("/yolo", response_model=YOLOResponse)
async def yoloPredict(file : UploadFile=File(...)): # 요청할 때 키값을 반드시 붙여서 보내야함!
    try:
        # 이미지 처리
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # filename = create_unique_imagename(file) # uuid, count, timestamp 파일명 생성
        filename = file.filename
        save_path = f'./images/{filename}'
        image.save(save_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"이미지 처리 중 오류가 발생했습니다: {e}")

    # 추론 모델로 예측
    # 이미지들의 경로를 리스트로 작성
    results = model.predict(save_path)

    if not results or not results[0].boxes.data.shape[0]:
        # 감지된 객체가 없을 경우 에러를 반환합니다.
        raise HTTPException(status_code=404, detail="감지된 객체가 없습니다.")

    result_image_path = f'./results/{filename}'
    results[0].save(result_image_path)
    
    # 저장된 결과 이미지를 Base64 문자열로 인코딩합니다.
    with open(result_image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 분류할 클래스 리스트
    class_names = results[0].names
    x1, y1, x2, y2, conf, cls = results[0].boxes.data[0]

    result_classname = [class_names[cls] for cls in results[0].boxes.cls.tolist()]
    result_score = [conf * 100 for conf in results[0].boxes.conf.tolist()]

    # 분류할 클래스 리스트
    print(f"name : {class_names[cls.item()]}")

    return YOLOResponse(name = result_classname, score = result_score, resultImage = encoded_string)

############################
############################
