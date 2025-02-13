FROM python:3.13-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y 

RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir -p /data && chmod 777 /data

EXPOSE 8000


CMD ["uvicorn", "main2:app" ,"--host" ,"127.0.0.1" ,"--port" ,"8000"]


## add npm, npx, uv