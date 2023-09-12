FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt --upgrade

COPY . /app/

RUN prisma generate

EXPOSE 8000

CMD [ "python", "server.py" ]