# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for Playwright (separate rarely-changing layers)
RUN apt-get update && apt-get install -y \
    wget \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to cache dependencies
COPY requirements.txt /app/requirements.txt

# Install Python dependencies (only rebuild if requirements.txt changes)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Playwright browsers and their dependencies (rarely changes)
RUN pip install playwright && playwright install --with-deps chromium

# Copy the rest of the application (frequently changing)
COPY . /app

# Set the command to run your application
CMD ["python", "run.py"]
