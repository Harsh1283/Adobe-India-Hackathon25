FROM python:3.10-slim

# Install system dependencies required for PyMuPDF and FAISS
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first (leverages Docker cache)
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Default command — modify the file names if needed
CMD ["python", "final_pipeline.py", "--input", "input/input.json", "--output", "output/output.json"]
