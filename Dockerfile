FROM python:alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
RUN rm -r ./requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8989"]
