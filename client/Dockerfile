FROM python:3.11.9
ADD . /client
VOLUME [ "/data" ]
WORKDIR /client
RUN python init.py
EXPOSE 7000
CMD [ "python", "main.py" ]