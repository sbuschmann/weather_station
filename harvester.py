import datetime as dt
import Adafruit_DHT as ada
import time 
import sys

sensor = ada.DHT22
pin = sys.argv[1]
i=0

now = dt.datetime.now().strftime(format="%Y%m%d_%H%M%S")
f = open("./data/weather_data_%s_%s.csv" %(pin, now), "a+")
header = "time,sensor,temp,hum\n"
f.write(header)

h_old = 0
h_new = 0
t_old = 0
t_new = 0

print("WeatherStation is running on pin %s ..." %pin)

while True:
	time.sleep(2)
	i +=1
	now = dt.datetime.now()	
	h_new, t_new = ada.read_retry(sensor, pin)

	h_new = "%.4f" %h_new
	t_new = "%.4f" %t_new

	if (h_new != h_old) or (t_new != t_old):
		line = "%s,%s,%s,%s\n" %(now, pin, t_new, h_new)
		f.write(line)
		f.flush()
		print("Pin %s: T or H changed to %s and %s at %s" %(pin, t_new, h_new, now))	
		h_old = h_new
		t_old = t_new
	else:
		print("T and H on pin %s unchanged" %pin)	

	if i == -10:
		break
f.close()
