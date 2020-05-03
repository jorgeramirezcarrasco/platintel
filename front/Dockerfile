FROM node:12.16.3

# Create app directory
WORKDIR /usr/src/app

ADD ./package*.json ./

RUN npm ci --only=production

# Bundle app source
ADD ./public ./public
ADD ./src ./src

EXPOSE 5000

# start app
RUN npm run build
RUN npm install -g serve
CMD serve -s build