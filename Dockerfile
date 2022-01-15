FROM python:3.9-alpine

LABEL maintainer="noaghzil615@gmail.com"

# apk设置国内更新源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && apk add --no-cache gcc musl-dev


COPY . /app

WORKDIR /app

# 更换pip源
RUN mkdir -p ~/.pip \ 
    && echo "[global]" > ~/.pip/pip.conf \
    && echo "index-url = https://mirrors.aliyun.com/pypi/simple/" >>  ~/.pip/pip.conf \
    && echo "[install]" >>  ~/.pip/pip.conf \
    && echo "trusted-host=mirrors.aliyun.com" >>  ~/.pip/pip.conf \
    && pwd \
    && ls \
    && ls tornado_demo/src \
    && sh install.sh

EXPOSE 6150

CMD ["/bin/sh", "/app/run.sh"]