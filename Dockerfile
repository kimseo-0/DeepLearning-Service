FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uvicorn fastapi

COPY src/fastapi_main.py .

COPY models/ /app/models/

COPY images/ /app/images/

EXPOSE 8080
CMD ["uvicorn", "src/fastapi_main:app", "--host", "0,0,0,0", "--port", "8080"]