FROM python:3.7

WORKDIR . 

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

ENTRYPOINT ["gunicorn","--bind","0.0.0.0:5000","wsgi:app"]