FROM python:3

RUN pip install clickhouse-driver requests

RUN mkdir -p /app
RUN mkdir -p /app/data
ADD functions.py /app/
ADD project.py /app/

CMD [ "python", "-u", "/app/project.py" ]