FROM python:3.9-alpine

LABEL maintainer="noaghzil615@gmail.com"

# apk设置国内更新源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && apk add --no-cache gcc musl-dev


COPY . /app

WORKDIR /app

# 更换pip源
RUN pwd \
    && ls \
    && ls tornado_demo/src \
    && sh install.sh

EXPOSE 6150

CMD ["/bin/sh", "/app/run.sh"]