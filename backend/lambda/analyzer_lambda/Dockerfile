FROM mcr.microsoft.com/playwright/python:v1.41.2-focal

WORKDIR /var/task

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Define the Lambda entrypoint
ENTRYPOINT ["/usr/bin/python3", "-m", "awslambdaric"]
CMD ["lambda_function.lambda_handler"]
