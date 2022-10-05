FROM node:alpine

ENV SLIDES_PORT $SLIDES_PORT

WORKDIR .

# Install dependencies
COPY ./package*.json ./

RUN npm install

COPY . .

EXPOSE $SLIDES_PORT

CMD [ "npm", "run", "dev"]