# Use a Python base image
FROM python:3.13-slim-bookworm

# Create data directory and set permissions
RUN mkdir -p /data
RUN chmod -R 777 /data

WORKDIR /app
# Install Node.js, npm, and npx
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates imagemagick git && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm npx && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install nvm (optional, if needed)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash


EXPOSE 8000

# Add and install UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Update PATH environment variable
ENV PATH="/root/.local/bin/:$PATH"

# Copy application files
COPY . /app/
RUN uv sync --frozen

# Start the application
CMD ["uv", "run", "main_final.py"]
