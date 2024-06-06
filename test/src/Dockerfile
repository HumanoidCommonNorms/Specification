ARG RUBY_VERSION=
ARG EXPOSE_PORT=8000

##=============================================================
# https://hub.docker.com/_/node/tags
#FROM node:latest
FROM node:lts-bullseye-slim
#FROM ruby:$RUBY_VERSIONslim
LABEL maintainer="Akari<masiro.to.akari@gmail.com>"
SHELL ["/bin/bash", "-c"]

##=============================================================
RUN apt update -q
RUN apt install -y build-essential locales zlib1g-dev
RUN apt install -y procps iputils-ping net-tools dnsutils iproute2 vim

##=============================================================
#RUN apt install -y nodejs
RUN apt install -y ruby-full
ENV GEM_HOME /root/gems
ENV PATH /root/gems/bin:$PATH
RUN gem install jekyll bundler webrick minima

##=============================================================
RUN sed -i -e "s/#alias l/alias l/g" /root/.bashrc
RUN sed -i -e "s/# alias l/alias l/g" /root/.bashrc

##=============================================================
WORKDIR /root/jekyll

COPY Gemfile /root/jekyll/Gemfile
RUN sed -i -e 's/\r//g' /root/jekyll/Gemfile

##=============================================================
RUN NOKOGIRI_USE_SYSTEM_LIBRARIES=true bundle install

RUN echo "en_US UTF-8" > /etc/locale.gen && locale-gen en-US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

##=============================================================
COPY entrypoint.sh /root/entrypoint.sh
RUN sed -i -e 's/\r//g' /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

##=============================================================
EXPOSE $EXPOSE_PORT

##=============================================================
ENTRYPOINT ["/root/entrypoint.sh"]
