FROM ubuntu:18.04 AS stock-service

RUN apt-get update -y
RUN apt-get install mongodb -y

WORKDIR /usr/src
COPY . .

RUN pip --version

RUN pip install -r requirements.txt
RUN chmod +x src/index.py

CMD ["python", "src/index.py"]