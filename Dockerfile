FROM python:3.10-slim
WORKDIR /app
COPY backend/app.py .
RUN pip install flask psycopg2
CMD ["python", "app.py"]
