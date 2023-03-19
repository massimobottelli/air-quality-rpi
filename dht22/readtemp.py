
import os
import time
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2

# read temp and humidity and append in csv
try:
    f = open('/home/pi/sensor/output/templog.csv', 'a+')
    if os.stat('/home/pi/sensor/output/templog.csv').st_size == 0:
            f.write('Date,Time,Temperature,Humidity\r\n')
except:
    pass

humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if humidity is not None and temperature is not None:
    f.write('{0},{1},{2:0.1f},{3:0.1f}\r\n'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M'), temperature, humidity))
    print ("temp = " + str(temperature) + "\nhumidity = " + str(humidity) + "\n")
else:
    print("Failed to retrieve data from sensor")
f.close()

# save time in .txt
f = open('/home/pi/sensor/output/time.txt', 'w+')
f.write('{0} - {1}'.format(time.strftime('%d/%m/%y'), time.strftime('%H:%M')))
f.close()

# save  temp in .txt
f = open('/home/pi/sensor/output/temperatura.txt', 'w+')
f.write('{0:0.1f}'.format(temperature))
f.close()

# save humidity in .txt
f = open('/home/pi/sensor/output/umidita.txt', 'w+')
f.write('{0:0.1f}'.format(humidity))
f.close()
