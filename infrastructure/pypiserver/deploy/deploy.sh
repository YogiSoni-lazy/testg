#!/bin/bash

if [ $(oc projects | grep -i jr-pypi | wc -l) -eq 0 ]; then
  oc new-project jr-pypi
fi
oc project jr-pypi
htpasswd -scb htpasswd pypi 'RedH@t123!!'
oc create secret generic htpasswd-secret --from-file htpasswd=htpasswd
rm htpasswd
oc create -f pypi-pvc.yml
oc create -f pypi-is.yml
oc create -f pypi-dc.yml
oc create -f pypi-svc.yml
oc create -f pypi-route.yml
