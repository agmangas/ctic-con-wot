FROM python:3.8-buster

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY main.py /opt/main.py

CMD ["python", "/opt/main.py"]