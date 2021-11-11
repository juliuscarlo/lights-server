#!/usr/bin/python3.7

"""Webserver for the lightroom control system """

# from flask_sqlalchemy import SQLAlchemy

from helper import Helper
from default_configs import DefaultConfig

from flask import Flask
from flask import request
from flask import render_template

from gpiozero import PWMLED
from gpiozero.pins.pigpio import PiGPIOFactory

from effects import Blink
from threading import Thread

from time import sleep

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route('/base_effect')
def slide_basefx():
    # Make sure that the currently running effect is stopped by setting aborted flag
    for i in range(10):
        config.aborted = True
        sleep(0.1)

    # sleep until all leds are off for 1 second

    slide_val = request.args.get('slide_val')
    effect = EffectSwitcher.effect_list()[int(slide_val)]
    config.effect = effect
    print(effect)

    config.aborted = False
    runner.run()

    return slide_val


@app.route('/stop_effect')
def stop_effect():
    config.aborted = True

    for client in config.clients:
        client.off()

    print("stop_effect")
    return "stop_effect"


@app.route('/default_effect')
def default_effect():
    effect_name = config.effect  # get the currently selected effect name
    # retrieve the corresponding standard settings dict
    default_settings = getattr(default_config, effect_name)
    for key, value in default_settings.items():  # unpack the dict to the instance attributes of the config
        setattr(config, key, value)

    print("default_effect")
    return "default_effect"


@app.route('/max_intensity_slider_value')
def slide_max_intensity():
    slide_val = request.args.get('slide_val')
    config.max_intensity = int(slide_val) / 1000
    print(slide_val)
    return slide_val


@app.route('/attack_slider_value')
def slide_attack():
    slide_val = request.args.get('slide_val')
    config.attack = int(slide_val) / 1000
    print(slide_val)
    return slide_val


@app.route('/decay_slider_value')
def slide_decay():
    slide_val = request.args.get('slide_val')
    config.decay = int(slide_val) / 1000
    print(slide_val)
    return slide_val


@app.route('/width_slider_value')
def slide_width():
    slide_val = request.args.get('slide_val')
    config.width = int(slide_val)
    print(slide_val)
    return slide_val


@app.route('/spacing_slider_value')
def slide_spacing():
    slide_val = request.args.get('slide_val')
    config.spacing = int(slide_val)
    print(slide_val)
    return slide_val


class EffectRunner:
    def __init__(self) -> None:
        self.switcher = EffectSwitcher()

    def run(self):
        while not config.aborted:
            effect = config.effect
            switcher_thread = Thread(
                target=self.switcher.select, args=(effect, config,))
            switcher_thread.start()
            switcher_thread.join()
            # config.automation_counter += 1

        # Reset aborted flag to False when the run loop is terminated
        config.aborted = False


class EffectSwitcher(object):
    """Provides a dispatch method to dynamically determine which effect
    function needs to be called during runtime."""
    @staticmethod
    def effect_list():
        """List available effects"""
        effect_list = [attribute for attribute in dir(EffectSwitcher) if callable(
            getattr(EffectSwitcher, attribute)) and attribute.startswith('__') is False and
            attribute is not 'select' and attribute is not 'effect_list']
        print(effect_list)
        return(effect_list)

    def select(self, argument, config):
        """Dispatch method"""
        method_name = str(argument)
        method = getattr(self, method_name, lambda: "Invalid effect.")
        return method(config)

    def strobe_sync(self, config):
        """Hard synced strobe effect (hard cut)."""
        Blink.simultaneous(config)

    def strobe_async(self, config):
        """Asynced strobe effect (hard cut)."""
        Blink.sequential(config)

    def strobe_random(self, config):
        Blink.random(config)

    def strobe_binary(self, config):
        """Binary strobe effect."""
        Blink.binary(config)

    def strobe_binary_sequential(self, config):
        """Binary sequential strobe effect."""
        Blink.binary_sequential(config)

    def glimmer_sync(self, config):
        """Glimmer effect, slowly turning on and off."""
        Blink.simultaneous(config)

    def glimmer_async(self, config):
        Blink.sequential(config)

    def glimmer_overlap(self, config):
        Blink.parallel(config)

    def standby(self, config):
        """shallow glimmer with pause."""
        Blink.simultaneous(config)

    def _off(self, config):
        for client in config.clients:
            client.off()

    def zpeziale(self, config):
        Blink.simultaneous(config)


class Automation:

    def __init__(self, target_attribute, upper_bound, lower_bound, step_size) -> None:
        self.target_attribute = target_attribute
        self.status = 'on'
        self.counter = 0
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.step = 1
        self.current_value = None

    def activate(self, config, target_attribute):
        if self.status == 'on':
            self.counter += 1
            self.current_value = getattr(config, target_attribute)
            if self.upper_bound > getattr(config, target_attribute):
                setattr(config, target_attribute, min())

    def deactivate(self, config, target_attribute):
        if target_attribute in Automation.automation_list:
            Automation.automation_list.remove(target_attribute)

    # use percentage values? probably best for width and spacing automation, (attack and decay)?

    @staticmethod
    def engage(self):
        pass

    @staticmethod
    def increment(self):
        pass

    @staticmethod
    def decrement(self):
        pass


class Attribute(Automation):
    def __init__(self) -> None:
        super().__init__()


def system_check(clients):
    for client in clients:
        client.blink(on_time=0.1, off_time=0.1,
                     fade_in_time=0.01,
                     fade_out_time=0.3, n=1,
                     background=False)
    for client in clients:
        client.blink(on_time=0.1, off_time=0.1,
                     fade_in_time=0.01,
                     fade_out_time=0.3, n=1,
                     background=True)

    print("System check complete...")


def initialize_gpio_clients():
    # remote gpio client settings
    clients = []

    try:
        client1 = PWMLED(pin=18, frequency=100,
                         pin_factory=PiGPIOFactory(host='pizero1.wlan'))
        clients.append(client1)
    except:
        print("Could not connect to client 1.")
    try:
        client2 = PWMLED(pin=18, frequency=100,
                         pin_factory=PiGPIOFactory(host='pizero2.wlan'))
        clients.append(client2)
    except:
        print("Could not connect to client 2.")
    try:
        client3 = PWMLED(pin=18, frequency=100,
                         pin_factory=PiGPIOFactory(host='pizero3.wlan'))
        clients.append(client3)
    except:
        print("Could not connect to client 3.")

    return clients


class Config:
    def __init__(self) -> None:
        self.clients = None

        self.effect = "strobe_sync"
        self.resolution = 1000
        self.attack = 0.002
        self.decay = 0.001
        self.curve = "lin"
        self.min_intensity = 0
        self.max_intensity = 1
        self.width = 0
        self.spacing = 500

        self.aborted = False


if __name__ == '__main__':
    config = Config()
    config.clients = initialize_gpio_clients()
    system_check(config.clients)

    default_config = DefaultConfig()

    aborted = Config()
    print('System initialized.')

    runner = EffectRunner()

    app.run(debug=False, host="192.168.4.1", port=5000)
    # app.run(debug=False, host="192.168.1.23", port=5000)
