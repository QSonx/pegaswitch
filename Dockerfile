FROM node:7
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN npm install
EXPOSE 53 80 8081
CMD [ "node", "start.js"  ]