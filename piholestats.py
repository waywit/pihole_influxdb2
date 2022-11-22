#! /usr/bin/python

# History:
# 2016: Script originally created by JON HAYWARD: https://fattylewis.com/Graphing-pi-hole-stats/
# 2016 (December) Adapted to work with InfluxDB by /u/tollsjo
# 2016 (December) Updated by Cludch https://github.com/sco01/piholestatus
# 2020 (March) Updated by http://cactusprojects.com/pihole-logging-to-influxdb-&-grafana-dash
# 2022 (November) Start work on update influxDBv2 compatibility

import requests
import time
# from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient
from influxdb_client .client.write_api import SYNCHRONOUS

# Setup your pihole enviroment
HOSTNAME = "pihole" # Pi-hole hostname to report in InfluxDB as tag for each measurement
PIHOLE_API = "http://xxx.xxx.xxx.xxx/admin/api.php" # Hostname or IP of PiHole

# Setup connection to your influxdbv2
INFLUXDB_URL = "http://xxx.xxx.xxx.xxx:8086" # Hostname or IP and Port of influxdb2 server
INFLUXDB_ORG = "my-org" # Organisation configured in influxdb2
INFLUXDB_TOKEN = "my-token" # Write token associated with correct user
INFLUXDB_BUCKET = "pihole" # Bucket to write data, can be changed. But the grafana dashbord is based on read-access to "pihole" bucket

def send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today):

	json_body = [
	    {
	        "measurement": "piholestats." + HOSTNAME.replace(".", "_"),
	        "tags": {
	            "host": HOSTNAME
	        },
	        "fields": {
	            "domains_blocked": int(domains_blocked),
                    "dns_queries_today": int(dns_queries_today),
                    "ads_percentage_today": float(ads_percentage_today),
                    "ads_blocked_today": int(ads_blocked_today)
	        }
	    }
	]

	#  Create influxDB client with write API, store data and close connection
	client = InfluxDBClient(INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG)
	write_api = client.write_api(write_options=SYNCHRONOUS)
	write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, json_body)
	client.close()

api = requests.get(PIHOLE_API) # URI to pihole server api
API_out = api.json()

# Parse information from pihole API
domains_blocked = (API_out['domains_being_blocked'])#.replace(',', '')
dns_queries_today = (API_out['dns_queries_today'])#.replace(',', '')
ads_percentage_today = (API_out['ads_percentage_today'])#
ads_blocked_today = (API_out['ads_blocked_today'])#.replace(',', '')

# Create JSON and it in influxdbv2
send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today)
