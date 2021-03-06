FROM python:3.8
COPY . /app/
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["python", "main.py", "--http"]