# bme280-exporter

A Prometheus exporter for the Bosch BME280 temperature, humidity, and pressure sensor, written in Python. Reads the sensor over I2C and serves metrics over HTTP through Flask and uWSGI.

## Contents

- `main.py` the exporter: opens the I2C connection and BME280 driver, registers `bme280_temperature_celsius`, `bme280_relative_humidity_percent`, and `bme280_pressure_hpa` gauges, and mounts the Prometheus WSGI app at `/metrics` alongside a `/` liveness route.
- `infra/uwsgi.ini` uWSGI configuration used to run the exporter in production.
- `infra/bme280-exporter.service` systemd unit template for running the exporter under uWSGI on a Raspberry Pi.

## Install

Requires Python >= 3.13 and uv.

```sh
git clone git@github.com:salimnassim/bme280-exporter.git
cd bme280-exporter
uv sync
```

Enable I2C on the Pi (`raspi-config` → Interface Options → I2C) and confirm the sensor is visible at its address:

```sh
i2cdetect -y 1
```

## Usage

The exporter expects a BME280 on I2C address `0x76` and assumes a sea-level pressure of `1013.25` hPa for the pressure calculation — both are hardcoded in `main.py`, adjust there if your board uses `0x77` or you need calibrated readings for your altitude.

```sh
uv run uwsgi infra/uwsgi.ini
```

or directly with Flask for local development:

```sh
uv run flask --app main run
```

Metrics are served at `http://<host>:5000/metrics`:

| Metric | Description |
| --- | --- |
| `bme280_temperature_celsius` | Temperature in °C |
| `bme280_relative_humidity_percent` | Relative humidity in % |
| `bme280_pressure_hpa` | Atmospheric pressure in hPa |

`/` returns `OK` and can be used as a liveness check.

```
# HELP bme280_temperature_celsius Temperature in Celsius
# TYPE bme280_temperature_celsius gauge
bme280_temperature_celsius 24.8037109375
# HELP bme280_relative_humidity_percent Relative humidity in percent
# TYPE bme280_relative_humidity_percent gauge
bme280_relative_humidity_percent 53.18778624729956
# HELP bme280_pressure_hpa Atmospheric pressure in hPa
# TYPE bme280_pressure_hpa gauge
bme280_pressure_hpa 1001.7279274409775
```

## Deploy as a systemd service

`infra/bme280-exporter.service` assumes the project is checked out at `/home/pi` and run as the `pi` user — adjust `WorkingDirectory`, `ExecStart`, and `User` to match your setup.

```sh
sudo cp infra/bme280-exporter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now bme280-exporter
```
