FROM python:3.10.0a6-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "/app/main.py"]