FROM python:3

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src/ ./src
COPY data/ ./data

EXPOSE 8050

CMD ["python", "src/dash_app.py"]
