import board
from adafruit_bme280 import basic as adafruit_bme280
from flask import Flask
from prometheus_client import Gauge, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

i2c = board.I2C()
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
bme280.sea_level_pressure = 1013.25

TEMPERATURE = Gauge("bme280_temperature_celsius", "Temperature in Celsius")
RELATIVE_HUMIDITY = Gauge(
    "bme280_relative_humidity_percent", "Relative humidity in percent"
)
PRESSURE = Gauge("bme280_pressure_hpa", "Atmospheric pressure in hPa")

TEMPERATURE.set_function(lambda: bme280.temperature)
RELATIVE_HUMIDITY.set_function(lambda: bme280.relative_humidity)
PRESSURE.set_function(lambda: bme280.pressure)

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})


@app.route("/")
def index():
    return "OK"
