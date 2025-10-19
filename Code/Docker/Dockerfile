FROM quay.io/centos/centos:stream9

RUN yum install -y wget bash net-tools strace iproute iputils net-tools pciutils vim procps-ng

WORKDIR /opt
COPY v3.06.tar.gz ./
RUN tar xfz v3.06.tar.gz

COPY bridged_trex_cfg.yaml /etc/
COPY routed_trex_cfg.yaml /etc/

COPY bridged_start.sh /
COPY routed_start.sh /
RUN chmod +x /bridged_start.sh
RUN chmod +x /routed_start.sh

CMD ["/bridged_start.sh"]
