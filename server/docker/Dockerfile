FROM node:latest
ADD ../ /view
WORKDIR /view
RUN sudo apt cnpm
RUN cnpm install 
EXPOSE 8080
CMD [ "npm", "run", "build"]
