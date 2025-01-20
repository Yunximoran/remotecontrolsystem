FROM node:latest
WORKDIR /view
ADD . /view
RUN npm install -g cnpm
RUN cnpm install 
EXPOSE 8080
VOLUME [ "/view" ]
CMD ["cnpm", "run", "serve"]
