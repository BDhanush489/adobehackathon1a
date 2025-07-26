# Use Python 3.10 slim image
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY process_pdfs.py .
COPY requirements.txt .
COPY sample-dataset ./sample-dataset

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run your script
CMD ["python", "process_pdfs.py"]
