FROM python:3.9

WORKDIR /app

COPY requirements.txt .
# Install dependencies with an increased timeout
RUN pip install --no-cache-dir -r requirements.txt --timeout=1500

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]