FROM centos
MAINTAINER Yuuki Enomoto <uki@e-yuuki.org>
RUN yum update -y && yum install -y \
    wget \
    gcc \
    gcc-c++ \
    ncurses-devel \
    zlib \
    zlib-devel \
    openssl-devel \
    libudev-devel
ENV PATH /usr/pkg/bin:/usr/pkg/sbin:$PATH
