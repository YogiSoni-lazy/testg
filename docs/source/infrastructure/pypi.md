# PyPI Servers


For intellectual property reasons, the DynoLabs packages are not available at [PyPI.org](https://pypi.org/).
Instead, we push (actually, Jenkins pushes) the packages to the following  Nexus PyPI servers that we manage and protect.

```{include} ../_templates/pypi_servers.md
```

## Installation Procedure Notes

:::{caution}
This section might be outdated and requires further review.
:::

### Standalone Server

The following installation procedure is for a standalone server. A
containerized approach is documented separately below. A large amount of
this code has been coded as an Ansible playbook at
`infrastructure/pypiserver/playbooks`

The SystemD considerations, Nginx, and SSL have not yet been put in the
playbook at this time.

- Install Nginx, httpd-tools

- Create user/group `pypiserver/pypiserver` with no login/no home directory

<!-- -->

    useradd -s /sbin/nologin -M -r -d /var/lib/pypiserver pypiserver

- Create directory /etc/pypiserver - root:pypiserver 0770

- Create password file: /etc/pypiserver/htpasswd -scb htpasswd
  \<username\> \<password\>

- chown root:pypiserver /etc/pypiserver/htpasswd ; chmod 0640

- Install python3, virtualenv

- Create virtualenv /usr/share/venv/pypiserver

- Create directory /var/lib/pypiserver root:pypiserver 0770

- Create directory /var/lib/pypiserver/packages root:pypiserver 0770

- pip install pypiserver passlib watchdog

- Server runtime options:

  - -p 8180

  - -i 127.0.0.1

  - -a update,download

  - -P /etc/pypiserver/htpasswd

  - -o

  - --log-file /var/lib/pypiserver/pypiserver.log

  - /var/lib/pypiserver/packages will be the package directory

- Lay down the /usr/lib/systemd/system/pypiserver.service file (see
  docs)

- systemctl daemon-reload

- enable and start pypiserver service

- Comment out default server on port 80 in /etc/nginx/nginx.conf

- mkdir -p /usr/share/nginx/cache

- chown root:nginx /usr/share/nginx/cache

- chmod 0770 /usr/share/nginx/cache

- give permission to nginx to talk to proxy at 8180

<!-- -->

    semanage port -a -t http_port_t -p tcp 8180
    semanage port -m -t http_port_t -p tcp 8180
    setsebool -P httpd_can_network_connect 1

- Configure nginx data cache for packages dir

- Create nginx configuration file in /etc/nginx/conf.d/pypiserver for
  80:proxypass

- Enable / Start nginx service

Configuring SSL (optional):

This all must be done before you proxypass to pypiserver …​certbot needs
to manipulate the standard nginx HTML files location for the Let’s
Encrypt challenge

- install certbot in Python virtual environment (version 1.6.0)

<!-- -->

    sudo su -
    source /usr/share/venv/pypiserver/bin/activate
    pip install certbot==1.6.0 certbot-nginx==1.6.0

- use certbot to get and configure nginx SSL cert using Let’s Encrypt

<!-- -->

    sudo su -
    mkdir -p /var/lib/pypiserver/certs/config
    mkdir -p /var/lib/pypiserver/certs/work
    mkdir -p /var/lib/pypiserver/certs/logs
    certbot certonly --nginx -n -d pypi.dev.nextcle.com \
      --email <your email address> --agree-tos \
      --config-dir=/var/lib/pypiserver/certs/config \
      --work-dir=/var/lib/pypiserver/certs/work \
      --logs-dir=/var/lib/pypiserver/certs/logs

- setup cronjob to daily execute certbot for renewal

<!-- -->

    sudo su -
    certbot renew --config-dir=/var/lib/pypiserver/certs/config

- configure nginx to support serving on port 443

      Update /etc/nginx/conf.d/pypiserver.conf

### Containerized Solution

Prequisites:

- docker or podman must be installed

      This script has only been tested on macOS.
      There are SELinux considerations for Linux.

- the docker daemon must be running

See the **Dockerfile** at *infrastructure/pypiserver/Dockerfile* for
details of how the server is configured. The container is configured
partially by Ansible so that the code can be reused on a standalone
server if needed.

To build and test the container:

    cd infrastructure/pypiserver
    ./test.sh
    cd ../../
    export PS_LOCAL_PASSWD=<pypi password - see Ansible code>
    make publish-local
    ls /tmp/packages

### Notes

- The htpasswd can be mounted from outside the container to control
  passwords externally. On OpenShift mounting a secret would be good for
  this.

- On OpenShift the volume for the packages should be a persistent volume


## Using the PyPI indexes

See the [publish guide](../contributors/core_publish.md) to learn how to release packages to the PyPI servers.

See the [quick start guide](../developers/quickstart.md) to learn how to install packages from the PyPI servers.
