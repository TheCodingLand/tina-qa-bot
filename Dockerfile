FROM python:slim-stretch

RUN apt-get update && apt-get install -y \
        build-essential \
        wget \
        git \
        python3-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

RUN mkdir -p /data/logs/
RUN mkdir -p /data/models/

WORKDIR /usr/src/app
ADD ./dl_models.py /usr/src/app
RUN python dl_models.py

ADD . /usr/src/app
#RUN pip install -r tina-requirements.txt
ENV PATH /usr/local/cuda/bin/:$PATH
ENV LD_LIBRARY_PATH /usr/local/cuda/lib:/usr/local/cuda/lib64
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"

CMD python3 main.py