FROM python:3.13.9-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 33000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "33000"]
