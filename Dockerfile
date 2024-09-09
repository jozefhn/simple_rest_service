FROM python:3.12-alpine
#FROM python:3.10-alpine
#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
WORKDIR /app/
#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY ./app ./app
CMD ["fastapi", "run", "app/main.py"]
