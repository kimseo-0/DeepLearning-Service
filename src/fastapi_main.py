from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel # 잘못된 형식의 데이터가 들어오는 경우 서버가 다운 되지 않도록 처리할 수 있게 도와주는 라이브러리
from typing import List
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import json

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# fast api 준비
app = FastAPI(title="ResNet34")

# 모델 준비
model = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
model.fc = nn.Linear(in_features=512, out_features=3, bias=True)
model.load_state_dict(torch.load('../models/celebrity_image_resnet34_model.pth', map_location='cpu'))
model.eval()
model.to(device)

# 추론용 전처리기
MEAN = (0.485, 0.456, 0.406)
STD = (0.229, 0.224, 0.225)
transforms_image = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN,STD)
])

class Response(BaseModel):
    name : str
    score : float
    type : int

# 예측 Api
@app.post("/predict", response_model=Response)
async def predict(file : UploadFile=File(...)): # 요청할 때 키값을 반드시 붙여서 보내야함!
    # 이미지 처리
    image = Image.open(file.file)
    image.save('../images/test.jpg') # 실제로는 이미지 이름을 uuid, count, timestamp 등을 사용
    image_tensor = transforms_image(image).unsqueeze(0).to(device)
    
    # 추론 모델로 예측
    with torch.no_grad():
        pred = model(image_tensor)
        print(f"예측값 : {pred}")
    
    pred_result = torch.max(pred, dim=1)[1].item() # 0, 1, 2
    score_list = nn.Softmax()(pred)[0] # [0.05, 0.9, 0.05], softmax 는 모든 값들의 합이 1이 되도록 조정해줌
    print(f"Softmax : {score_list}")
    score = float(score_list[pred_result])

    # 분류할 클래스 리스트
    classname = ['마동석', '이수지', '카리나']
    name = classname[pred_result]
    print(f"name : {name}")

    return Response(name = name, score = score, type = pred_result)