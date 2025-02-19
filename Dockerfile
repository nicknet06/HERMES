FROM alpine:latest



# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nginx \
    build-base \
    python3-dev \
    curl

# Set working directory
WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY src/ .
COPY nginx.conf /etc/nginx/nginx.conf

# Create necessary directories and set permissions
RUN mkdir -p /data /app/audio_uploads && \
    chown -R nobody:nobody /data /app/audio_uploads

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# Command to run the application
CMD ["sh", "-c", "nginx && python3 app.py"]