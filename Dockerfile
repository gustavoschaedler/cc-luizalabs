FROM python:alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apiluizalabs ./apiluizalabs
RUN rm -r ./requirements.txt

# Executa como usuario nao root (seguraca)
RUN adduser -D appuser
USER appuser

CMD ["uvicorn", "apiluizalabs.main:app", "--host", "0.0.0.0", "--port", "8989"]
