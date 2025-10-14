FROM quay.io/centos/centos:stream9

RUN yum install -y wget bash net-tools strace iproute iputils net-tools pciutils vim procps-ng

WORKDIR /opt
COPY v3.06.tar.gz ./
RUN tar xfz v3.06.tar.gz

COPY trex_cfg.yaml /etc/

COPY start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
