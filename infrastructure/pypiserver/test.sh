#!/bin/sh
# Only tested on a Mac
# There are selinux considerations for Linux
docker run -d -p 8180:8180 -v /tmp/packages:/var/lib/pypiserver/packages pypi
