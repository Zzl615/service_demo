#!/bin/bash
echo $0
work_path=$(pwd)
echo ${work_path}
python3.9 -m venv ${work_path}/env
${work_path}/env/bin/python3.9 -m pip install --no-cache-dir --upgrade pip setuptools
${work_path}/env/bin/pip install --no-cache-dir -r requirements.txt  -i   https://mirrors.aliyun.com/pypi/simple/