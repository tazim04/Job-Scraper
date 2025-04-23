FROM mcr.microsoft.com/playwright/python:v1.41.2-focal

# Set workdir
WORKDIR /var/task

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Lambda-compatible handler
CMD ["lambda_function.lambda_handler"]
