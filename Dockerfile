FROM python:3.9-alpine

LABEL maintainer="noaghzil615@gmail.com"

COPY . /app

WORKDIR /app

# 更换pip源
RUN pwd \
    && ls \
    && ls tornado_demo/src \
    && sh install.sh

EXPOSE 6150

CMD ["/bin/sh", "/app/run.sh"]