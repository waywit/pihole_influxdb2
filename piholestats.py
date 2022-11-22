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
from influxdb_client import InfluxDBClient, Point, WriteOptions

HOSTNAME = "pihole" # Pi-hole hostname to report in InfluxDB for each measurement
PIHOLE_API = "http://xxx.xxx.xxx.xxx/admin/api.php" # IP of PiHole
INFLUXDB_SERVER = "http://xxx.xxx.xxx.xxx:8086" # IP or hostname to InfluxDB server
# INFLUXDB_PORT = 8086 # Port on InfluxDB server
# INFLUXDB_USERNAME = ""
# INFLUXDB_PASSWORD = ""
# INFLUXDB_DATABASE = "dev_pihole"
DELAY = 10 # seconds

# influxdb v2 settings
INFLUXDB_ORG = ""
INFLUXDB_TOKEN = ""
INFLUXDB_BUCKET = "dev_pihole"

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

	# remove: client = InfluxDBClient(INFLUXDB_SERVER, INFLUXDB_PORT, INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DATABASE) # InfluxDB host, InfluxDB port, Username, Password, database
	# Setup new influxDB Client from config file "config.ini"
	client = InfluxDBClient(INFLUXDB_SERVER, INFLUXDB_TOKEN, INFLUXDB_ORG)
	# remove: client.create_database(INFLUXDB_DATABASE) # Uncomment to create the database (expected to exist prior to feeding it data)
	client.write(INFLUXDB_BUCKET, INFLUXDB_ORG, json_body)

api = requests.get(PIHOLE_API) # URI to pihole server api
API_out = api.json()

#print (API_out) # Print out full data, there are other parameters not sent to InfluxDB

domains_blocked = (API_out['domains_being_blocked'])#.replace(',', '')
dns_queries_today = (API_out['dns_queries_today'])#.replace(',', '')
ads_percentage_today = (API_out['ads_percentage_today'])#
ads_blocked_today = (API_out['ads_blocked_today'])#.replace(',', '')

send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today)
