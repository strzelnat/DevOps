FROM python:3.11-slim

WORKDIR /app

COPY web.py .

EXPOSE 8080

CMD ["python", "web.py"]
