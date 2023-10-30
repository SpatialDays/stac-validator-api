FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
# cmd gunicorn stac_validator:app on port 80
CMD ["gunicorn", "app:app" ,"--bind", "0.0.0.0:80"]