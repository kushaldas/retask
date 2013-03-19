.. redissetup:

Setting up the Redis Server
===========================
You can download and install `Redis <http://redis.io>`_ on your distro.

In `Fedora <http://fedoraproject.org>`_ you can just ``yum install redis``
for the same.

To start the server in the local folder use the following command:

::

    $ redis-server

On Fedora you can start the service as *root*:

::

    # systemctl enable redis.service
    # systemctl start redis.service

In `Debian <http://debian.org>`_ just install the redis-server package with
``apt-get install redis-server`` to have a redis server running.

