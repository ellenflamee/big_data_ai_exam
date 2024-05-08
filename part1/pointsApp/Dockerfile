FROM python:3.12.0-alpine

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5000 (assuming your Flask app runs on port 5000)
EXPOSE 5000

CMD ["python", "app.py"]