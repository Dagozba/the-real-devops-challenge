FROM python:3.6

WORKDIR /app

COPY app.py requirements.txt /app/

#https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#add-or-copy
COPY src/*.py /app/src/

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "app.py", "-h"]

