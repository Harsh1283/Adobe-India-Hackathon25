# Set the base image and platform
FROM --platform=linux/amd64 python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy your local files into the container
COPY requirements.txt .
COPY process_pdf.py .

# Run commands to install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run when the container starts
CMD ["python", "process_pdf.py"]