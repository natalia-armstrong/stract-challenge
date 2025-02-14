FROM python:3.9-slim

WORKDIR /stract

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY config.env .env

EXPOSE 5000

CMD ["python", "src/app.py"]
