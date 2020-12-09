FROM python:3
WORKDIR /app

RUN pip3 install --upgrade flask pika requests elasticsearch \
    google-cloud-logging google-cloud-storage google-cloud-vision kafka-python 

ADD ./app.py /app/app.py
ADD ./gcp_utils.py /app/gcp_utils.py
ADD ./constants.py /app/constants.py

CMD ["python","app.py"]