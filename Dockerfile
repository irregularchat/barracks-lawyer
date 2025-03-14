FROM python:3.9-slim

# Set the XDG_RUNTIME_DIR environment variable
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

# Create the runtime directory with proper permissions
RUN mkdir -p /tmp/runtime-root && chmod 777 /tmp/runtime-root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev

WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

EXPOSE 8507

CMD ["gradio", "app.py"]
