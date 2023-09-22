#!/bin/bash

# Ejecuta el comando speedtest-cli y redirige la salida al archivo log
fecha_hora=$(date +"%Y-%m-%d %H:%M:%S")
echo $fecha_hora
/usr/bin/python3 /home/pi/selenium-py/scraper.py
echo terminado
