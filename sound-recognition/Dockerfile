FROM ubuntu:18.04

ARG REACT_APP_MQTT_URL=mqtt://localhost:9001
ENV REACT_APP_MQTT_URL $REACT_APP_MQTT_URL

ENV PATH_APP /opt/app

RUN apt-get update -y && apt-get install curl -y
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

RUN mkdir -p ${PATH_APP}
WORKDIR ${PATH_APP}

COPY . .

RUN npm install 
#--legacy-peer-deps

# RUN npm run build 

EXPOSE 3000

CMD ./start.sh