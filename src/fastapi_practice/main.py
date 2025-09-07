# 모듈 설치 : uv add fastapi uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "메롱😛"}

@app.get("/image")
def make_image():
    return {"result":"카리나"}

@app.get("/chatbot")
def make_image():
    return {"result":"안녕하세요 저는 chatGPT 입니다"}

@app.get("/video")
def make_image():
    return {"result":"동영상 생성 완료"}

# 로컬 : 내 PC에서만 돌아가게 하고 싶다면?
# uvicorn main:app --reload --port 8080
# 127.0.0.0:8080

# 내 ip 주소 확인하기
# 'ipconfig'
# 이더넷 어댑터 이더넷 : IPv4 주소

# 외부 접속 : 외부에서 접속할 수 있게 하고 싶다면?
# 단, 동일 네트워크 내에서만 가능 (동일 공유기 또는 랜)
# uvicorn main:app --host 0.0.0.0 --port 9000
# 'ipv4주소:포트번호' 로 접속

# HTML
templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: int):
    return templates.TemplateResponse("./index.html", {"request": request, "id": id})