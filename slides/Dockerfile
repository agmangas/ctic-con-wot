FROM node:alpine

ENV SLIDES_PORT $SLIDES_PORT

RUN mkdir -p ./app
WORKDIR app

# Install dependencies
COPY ../package*.json .

RUN npm install

COPY .. .

EXPOSE $SLIDES_PORT

CMD [ "npm", "run", "dev"]