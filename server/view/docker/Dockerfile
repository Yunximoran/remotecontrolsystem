FROM node:latest as build-stage
ADD ../ /view
WORKDIR /
RUN  npm install
CMD [ "npm", "run", "build" "--port", "8080"]