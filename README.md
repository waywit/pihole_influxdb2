# Install dependencies (python3-influxDB2-client)

1. Setup python3 and influxDB client from influxdata. Install "pip" on your system:
```
  $ sudo apt install pip
```
2. To install the InfluxDB Python Client Library, simply run:
```
  $ pip install influxdb-client
```
3. If you already have the client installed, you can upgrade it with:
```
  $ pip3 install --upgrade influxdb-client
```

# Client configuration

Edit the "piholestats.py" file with en editor of your choice:

You need to configure your individual pihole settings;
```
  # Setup your pihole enviroment
  HOSTNAME = "pihole" # Pi-hole hostname to report in InfluxDB as tag for each measurement
  PIHOLE_API = "http://xxx.xxx.xxx.xxx/admin/api.php" # Hostname or IP of PiHole
```
Then you also need to configure your influxDBv2 system, we will need a write access token to the defined bucket in the organisation:
```
  # Setup connection to your influxdbv2
  INFLUXDB_URL = "http://xxx.xxx.xxx.xxx:8086" # Hostname or IP and Port of influxdb2 server
  INFLUXDB_ORG = "my-org" # Organisation configured in influxdb2
  INFLUXDB_TOKEN = "my-token" # Write token associated with correct user
  INFLUXDB_BUCKET = "pihole" # Bucket to write data, can be changed. But the grafana dashbord is based on read-access to "pihole" bucket
```

# Test and rollout

You can test your configuration by running:
```
  $ python3 piholestats.py
```
And then check your influxDB bucket if you have received the first values:

- ads_blocked_today
- ads_percentage_today
- dns_queries_today
- domains_blocked

Best idea is to run it as a cronjob, so call
```
  $ crontab -e
```
And insert the following line to execute the script every minute:
```
  */1 * * * * /usr/bin/python3 /home/proxmox/bin/pihole_influxdb2/piholestats.py >/dev/null 2>&1
```
# grafana setup

You need to connect the influxDBv2 in grafana using the "flux" language (not the opd influxQL). You will need read token to the configured bucket. Then you can import the "grafana/pihole_grafana.json".
