FROM node:12.16.3

# Create app directory
WORKDIR /usr/src/app

ADD ./package*.json ./

RUN npm ci --only=production

# Bundle app source
ADD ./server ./server

EXPOSE 8000

CMD [ "node", "./server/server.js" ]