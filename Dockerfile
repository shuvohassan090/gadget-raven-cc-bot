# Base image (Python 3.11)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to working directory
COPY . .

# Expose port (যদি ওয়েব সার্ভার থাকে; না থাকলে এটা চাই না)
# EXPOSE 8080

# Command to run your bot/app
CMD ["python", "bot.py"]
