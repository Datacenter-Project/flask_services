FROM python:3
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./app.py /app/app.py
ADD ./gcp_utils.py /app/gcp_utils.py
ADD ./constants.py /app/constants.py

CMD ["python","app.py"]