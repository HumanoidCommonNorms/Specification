ARG RUBY_VERSION=
ARG SERVER_PORT=4000

##=============================================================
# https://hub.docker.com/_/node/tags
#FROM node:latest
#FROM node:lts-bullseye-slim
FROM ruby:${RUBY_VERSION}slim
LABEL maintainer="Akari<masiro.to.akari@gmail.com>"
SHELL ["/bin/bash", "-c"]

##=============================================================
RUN apt update -q
RUN apt install -y sudo
RUN apt install -y ruby-full build-essential locales zlib1g-dev
# RUN apt install -y nodejs

RUN apt install -y procps iputils-ping net-tools dnsutils vim

##=============================================================
ENV GEM_HOME /root/gems
ENV PATH /root/gems/bin:$PATH
RUN gem install jekyll bundler webrick minima

##=============================================================
RUN sed -i -e "s/#alias l/alias l/g" /root/.bashrc
RUN sed -i -e "s/# alias l/alias l/g" /root/.bashrc

##=============================================================
WORKDIR /root/jekyll

COPY Gemfile /root/jekyll/Gemfile

##=============================================================
RUN NOKOGIRI_USE_SYSTEM_LIBRARIES=true bundle install

RUN echo "en_US UTF-8" > /etc/locale.gen && \
    locale-gen en-US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

##=============================================================
#COPY entrypoint.sh /entrypoint.sh

##=============================================================
EXPOSE ${SERVER_PORT}

##=============================================================
# ENTRYPOINT ["/entrypoint.sh"]
# ENTRYPOINT ["bundle","exec","jekyll","serve","--config","/root/jekyll/_config.yml"]
