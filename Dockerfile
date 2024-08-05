FROM python:3.10-bullseye

ENV TZ Asia/Shanghai
ENV school_robot_docker_mode 1

WORKDIR school-robot

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y libgbm-dev libgtk-3-0 --fix-missing && \
    git clone https://github.com/School-Robot/Plugin-Loader.git && \
    pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple && \
    pip install --upgrade pip \
    pip install websocket-client 


#TESTING
# COPY . /school-robot

COPY ./docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash","/entrypoint.sh"]