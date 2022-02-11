FROM python:3.8


WORKDIR /app
COPY . /app

ENV APP_CONFIG=gunicorn_config.py
RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["wsgi.py", "flask", "run"]

