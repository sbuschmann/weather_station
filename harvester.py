#stephan

import datetime as dt
import Adafruit_DHT as ada
import time
import sys
import numpy as np

sensor = ada.DHT22
pins = [4,17]
i=0

now = dt.datetime.now().strftime(format="%Y%m%d_%H%M%S")
f = open("./data/weather_data_%s.csv" %(now), "a+")
header = "time,sensor,temp,hum\n"
f.write(header)

nPins = len(pins)

h_old = np.zeros(nPins)
h_new = np.zeros(nPins)
t_old = np.zeros(nPins)
t_new = np.zeros(nPins)

print("WeatherStation is running ...")

while True:
	#time.sleep(10)
	i +=1
	now = dt.datetime.now()

	for i in range(0,nPins):
		pin = pins[i]

		h_new[i], t_new[i] = ada.read_retry(sensor, pin)

		h_new[i] = "%.4f" %h_new[i]
		t_new[i] = "%.4f" %t_new[i]

		if (h_new[i] != h_old[i]) or (t_new[i] != t_old[i]):
			line = "%s,%s,%s,%s\n" %(now, pin, t_new[i], h_new[i])
			f.write(line)
			f.flush()
			print("Pin %s: T or H changed to %s and %s at %s" %(pin, t_new[i], h_new[i], now))
			h_old[i] = h_new[i]
			t_old[i] = t_new[i]
		else:
			print("T and H on pin %s unchanged" %pin)
	time.sleep(10)
f.close()
