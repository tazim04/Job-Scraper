FROM mcr.microsoft.com/playwright/python:v1.41.2-focal

# Set workdir
WORKDIR /var/task

# Install Lambda Runtime Interface Emulator
# ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/local/bin/aws-lambda-rie
# RUN chmod +x /usr/local/bin/aws-lambda-rie

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Use RIE to run Lambda handler
# ENTRYPOINT ["/usr/local/bin/aws-lambda-rie"]
# CMD ["python3", "-m", "awslambdaric", "lambda_function.lambda_handler"]

CMD ["lambda_function.lambda_handler"]