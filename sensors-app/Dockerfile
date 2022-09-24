FROM python:3.8-buster

ENV PATH_APP /opt/app

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get update -y && apt-get install -y nodejs

RUN mkdir -p ${PATH_APP}
WORKDIR ${PATH_APP}
COPY . .
RUN ./build-app.sh
WORKDIR ${PATH_APP}/api
RUN pip install .

EXPOSE 5000

CMD /opt/app/start.sh
