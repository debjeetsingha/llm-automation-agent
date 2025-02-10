FROM python:3.13-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y 

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Run the FastAPI application by default
# Uses `fastapi dev` to enable hot-reloading when the `watch` sync occurs
# Uses `--host 0.0.0.0` to allow access from outside the container
# CMD ["fastapi", "run", "--host", "127.0.0.1", "main.py","--port", "8000"]

CMD ["uvicorn", "main:app" ,"--host" ,"127.0.0.1" ,"--port" ,"8000"]
