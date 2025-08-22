import torch
import torch.nn as nn
from torchvision.transforms import transforms
from torchvision import models
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

class_names = ["마동석", "카리나", "이수지"]

# 모델 준비

@st.cache_resource
def load_model():
    model = models.resnet34(pretrained=False)
    model.fc = nn.Linear(512,3)
    model.load_state_dict(torch.load("models/celebrity_image_resnet34_model.pth"),map_location=torch.device('cpu'))
    model.eval()
    return model

# 추론용 전처리기
def transfor_image(image):
    MEAN = (0.485, 0.456, 0.406)
    STD = (0.229, 0.224, 0.225)

    transforms_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(MEAN,STD)
    ])

    return transforms_test(image).unsqueeze(0)

st.title("연예인분류기 v.1")
upload_file = st.file_uploader('이미지를 업로드하세요', type=['jpg', 'jpeg', 'png'])

if upload_file is not None: 
    image = Image.open(upload_file).convert('RGB')
    st.image(image, caption="업로드 이미지", use_column_width=True)

    model = load_model()
    infer_img = transfor_image(image)

    with torch.no_grad():
        result = model(infer_img)
        preds = torch.max(result, dim = 1)[1]
        pred_classname = class_names[preds.item()]
        confidence = torch.softmax(result,dim=1)[0][preds.item()].item() * 100

    st.success(f'예측결과: {pred_classname} ({confidence:.2f}% 확신)')