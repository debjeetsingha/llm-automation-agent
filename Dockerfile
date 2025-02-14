FROM python:3.13-slim-bookworm

WORKDIR /app

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates imagemagick git 

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

RUN uv sync --frozen

# RUN pip install --no-cache-dir -r requirements.txt

# Download and install nvm:
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# in lieu of restarting the shell
ENV NVM_DIR="$HOME/.nvm"
RUN . "$NVM_DIR/nvm.sh" && \
    nvm install 22 && \
    nvm use 22 && \
    npm install -g npx


RUN mkdir -p /data && chmod 777 /data

EXPOSE 8000

COPY . /app/

# CMD ["uvicorn", "main2:app" ,"--host" ,"127.0.0.1" ,"--port" ,"8000"]
CMD ["uv", "run", "main_final"]

## add npm, npx, uv