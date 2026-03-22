FROM python:3.11-slim

WORKDIR /app

RUN pip install flask

COPY test_server.py .

ENV PORT=8000
ENV SERVER_ID=unknown

CMD ["python", "test_server.py"]
