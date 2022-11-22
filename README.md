1. Setup python influxDB client from influxdata

Install "pip" on your system:

  $ sudo apt install pip

2. To install the InfluxDB Python Client Library, simply run:

  $ pip install influxdb-client

3. If you already have the client installed, you can upgrade it with:

  $ pip3 install --upgrade influxdb-client




Client configuration
--------------------

Via File
^^^^^^^^
A client can be configured via ``*.ini`` file in segment ``influx2``.

The following options are supported:

- ``url`` - the url to connect to InfluxDB
- ``org`` - default destination organization for writes and queries
- ``token`` - the token to use for the authorization
- ``timeout`` - socket timeout in ms (default value is 10000)
- ``verify_ssl`` - set this to false to skip verifying SSL certificate when calling API from https server
- ``ssl_ca_cert`` - set this to customize the certificate file to verify the peer
- ``cert_file`` - path to the certificate that will be used for mTLS authentication
- ``cert_key_file`` - path to the file contains private key for mTLS certificate
- ``cert_key_password`` - string or function which returns password for decrypting the mTLS private key
- ``connection_pool_maxsize`` - set the number of connections to save that can be reused by urllib3
- ``auth_basic`` - enable http basic authentication when talking to a InfluxDB 1.8.x without authentication but is accessed via reverse proxy with basic authentication (defaults to false)
- ``profilers`` - set the list of enabled `Flux profilers <https://docs.influxdata.com/influxdb/v2.0/reference/flux/stdlib/profiler/>`_

.. code-block:: python

    self.client = InfluxDBClient.from_config_file("config.ini")

.. code-block::
