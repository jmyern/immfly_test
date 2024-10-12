FROM python:3.12-alpine3.20
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

RUN addgroup -S app && adduser -S app -G app
USER app

CMD ["gunicorn", "-c", "gunicorn.conf.py", "immfly.wsgi"]
