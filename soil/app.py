import time
from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

from counterfit_shims_seeed_python_grove.grove_adc import GroveADC

adc = GroveADC()

while True:
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)
    time.sleep(10)