#!/usr/bin/python3
import os
import json
import sys
import datetime
from influxdb import InfluxDBClient

host = '127.0.0.1'
username = 'admin'
pass = 'yourinfluxdbpass'

client = InfluxDBClient(host=host, port=8086, username=username, password=pass)
client.switch_database('stats')

date = os.popen("date +%s").read().split('\n')
time = ((int(date[0])) * 1000000000 - 10000000000)
hn = os.popen("hostname").read().split('\n')
nstat = os.popen("nstat -a --json").read()
data = json.loads(nstat) 
info = ''
for i in data.keys():
	info = i
fields = (data[info])
influx_data = []
influx_data.append(
	{
		"measurement": "nstats",
		"tags": {
			"hostname" : hn[0]
		},
		"time": time,
		"fields": fields
		}
	)
client.write_points(influx_data)
