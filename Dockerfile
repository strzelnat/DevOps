FROM python:3.11-slim

WORKDIR /app

COPY server.py .
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
RUN pip install mysql-connector-python

EXPOSE 8080

CMD ["./wait-for-it.sh", "mysql-db:3306", "--", "python", "server.py"]
