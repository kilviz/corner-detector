FROM python

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /src && \
    mkdir -p /src/public/static && \
    mkdir -p /src/public/media

WORKDIR /src/app

RUN git clone https://github.com/kilviz/corner-detector.git /src/app


RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /src/app/backend

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN  DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --noinput --username admin --email example@gmail.com
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
