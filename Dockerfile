FROM python:3

RUN pip install clickhouse-driver

ADD functions.py /app
ADD project.py /app

CMD [ "python", "-u", "./project.py" ]