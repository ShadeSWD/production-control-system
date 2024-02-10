FROM python:3.12

ENV PYTHONUNBUFFERED 1

RUN mkdir production_control_system

WORKDIR production_control_system

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .


RUN chmod a+x docker/*.sh
