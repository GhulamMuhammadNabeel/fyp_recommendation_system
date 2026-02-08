# 1️⃣ Base image
FROM python:3.12-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Copy only requirements first (cache layer)
COPY requirements.txt .

# 4️⃣ Install dependencies

RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy backend code
COPY . .

# 6️⃣ Expose port for FastAPI
EXPOSE 8000

# 7️⃣ Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
