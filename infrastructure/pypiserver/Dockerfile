FROM registry.access.redhat.com/ubi8/ubi:8.2

LABEL maintainer="Jim Rigsbee <jrigsbee@redhat.com>" \
      io.k8s.description="PyPI Server" \
      io.k8s.display-name="PyPI Server 1.3" \
      io.openshift.expose-services="8180:http"

RUN dnf update -y && \
    dnf install -y python3 python3-pip python3-virtualenv && \
    dnf clean all

WORKDIR /root
ADD playbooks ./playbooks
RUN pip3 install -q ansible==2.9 && \
    ansible-playbook playbooks/site.yml && \
    rm -fr playbooks && \
    pip3 uninstall -yq ansible && \
    chown -R pypiserver:0 /etc/pypiserver && \
    chmod -R g=u /etc/pypiserver

USER pypiserver
WORKDIR /var/lib/pypiserver

EXPOSE 8180
VOLUME /var/lib/pypiserver/packages

ENTRYPOINT source /usr/share/venv/pypiserver/bin/activate && pypi-server -p 8180 -a update,list -o -i 0.0.0.0 --log-file /dev/null -P /etc/pypiserver/htpasswd /var/lib/pypiserver/packages
