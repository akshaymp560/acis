# 1. Start with a lightweight version of Python
FROM python:3.11-slim

# 2. Create a folder inside the cloud server called /app
WORKDIR /app

# 3. Copy ONLY the requirements file first 
COPY requirements.txt .

# 4. Install the Python libraries 
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your Python code and HTML templates
COPY . .

# 6. Open port 8000 so the internet can reach your app
EXPOSE 8000

# 7. Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]