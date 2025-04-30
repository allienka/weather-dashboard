# Use specific Python version for stability
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Configure Finnish locale
RUN echo "fi_FI.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LANG=fi_FI.UTF-8
ENV LANGUAGE=fi_FI:fi
ENV LC_ALL=fi_FI.UTF-8

# Copy Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose Dash port (this allows connections from outside the container)
EXPOSE 8050

# Run the app with python3, ensuring it listens on all IPs and the correct port
CMD ["python3", "app.py"]
