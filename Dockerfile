FROM python:3.7-slim
# MAINTAINER Mykhailo Lazoryk  # автор образа

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# RUN  запускает команду только для конкретно этого образа
RUN pip install -r /requirements.txt

# дальше создадим папку app, которую сделаем основной и поместим туда содержимое наших папок
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# добавим нашего пользователя
RUN adduser user

# укажем нашему приложение использовать только что созданного user как главного
USER user