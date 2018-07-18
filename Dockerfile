FROM python:3.6-alpine

RUN mkdir -p /bot/box 
WORKDIR /bot/

RUN apk add --no-cache bash gcc gfortran  build-base 
RUN pip install slackclient plotly numpy

COPY . /bot
ENV SLACK_CHANNEL="#general" 
#ENV CA_DN="CA_default" 

#ENTRYPOINT python
CMD python