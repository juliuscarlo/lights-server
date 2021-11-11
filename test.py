#!/usr/bin/python3.7

"""Webserver for the lightroom control system """

# from flask_sqlalchemy import SQLAlchemy
import threading
import random

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

import math

import gpiozero
from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory

from multiprocessing import Manager
from threading import Thread
from time import sleep
from datetime import datetime

import time

# client gpio and IP settings
client1 = PWMLED(pin=18, frequency=100,
                 pin_factory=PiGPIOFactory(host='pizero1.wlan'))
client2 = PWMLED(pin=18, frequency=100,
                 pin_factory=PiGPIOFactory(host='pizero2.wlan'))
client3 = PWMLED(pin=18, frequency=100,
                 pin_factory=PiGPIOFactory(host='pizero3.wlan'))

clients = [client1, client2, client3]

for client in clients:
    client.value = 0

for i in range(99):
    for client in clients:
        client.value += 0.01
