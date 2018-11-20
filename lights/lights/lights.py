# Lights Controller and light patterns
# Phil Hansen, 22 October 2016
# Copyright Notice

import logging
import os
import random
import signal
import time
import RPi.GPIO as GPIO

import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

from multiprocessing import Process
import config

# list of the known patterns
patterns = [
    'chase_up',
    'chase_down',
    'fill_up',
    'fill_down',
    'fill_up_and_down',
    'fill_up_chase_up',
    'alternating',
    'random_sets',
    'random_on_off',
    'appear_from_back',
    'fade_in_out',
    'rainbow_colors',
    'rainbow_cycle',
    ]

# list of the lights to use in patterns
pattern_lights = range(0, config.pixel_count)

SPI_PORT   = 0
SPI_DEVICE = 0

class LightsController(object):
    """Contains functions for controlling the lights"""

    # the process for running pattern functions
    process = None

    # the Adafruit WS2801 pixels object
    pixels = None
    
    @staticmethod
    def setup():
        """Setup the interfaces"""
        LightsController.pixels = Adafruit_WS2801.WS2801Pixels(config.pixel_count, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)
        LightsController.pixels.clear()
        LightsController.pixels.show()
        
    @staticmethod
    def off(lights=None, stop_existing=True):
        """Turn off all lights in the given list
           Default all
           Set stop_existing to False to skip stopping the existing process
        """
        if stop_existing:
            LightsController.stop_existing_process()
        if lights is None:
            LightsController.pixels.clear()
        else:
            for i in lights:
                LightsController.pixels.set_pixel_rgb(i, 0, 0, 0)
        LightsController.pixels.show()
    
    @staticmethod
    def on(lights=None, stop_existing=True):
        """Turn on all lights in the given list
           Default all
           Set stop_existing to False to skip stopping the existing process
        """
        if stop_existing:
            LightsController.stop_existing_process()
        if lights is None:
            LightsController.set_color()
        else:
            for i in lights:
                if config.is_rbg:
                    LightsController.pixels.set_pixel_rgb(i, config.color['r'], config.color['b'], config.color['g'])
                else:
                    LightsController.pixels.set_pixel_rgb(i, config.color['r'], config.color['g'], config.color['b'])
            LightsController.pixels.show()
    
    @staticmethod
    def set_color(light=None, show=True):
        """Set a specific led or all leds to the current color
           Set show to False to skip calling pixels.show()
        """
        if config.is_rbg:
            if light is None:
                LightsController.pixels.set_pixels_rgb(config.color['r'], config.color['b'], config.color['g'])
            else:
                LightsController.pixels.set_pixel_rgb(light, config.color['r'], config.color['b'], config.color['g'])
        else:
            if light is None:
                LightsController.pixels.set_pixels_rgb(config.color['r'], config.color['g'], config.color['b'])
            else:
                LightsController.pixels.set_pixel_rgb(light, config.color['r'], config.color['g'], config.color['b'])
        if show:
            LightsController.pixels.show()
    
    @staticmethod
    def get_random_color():
        """Gets a random color - RGB values"""
        color = {
            'r': random.randint(0, 255),
            'g': random.randint(0, 255),
            'b': random.randint(0, 255)
        }
        return color

    @staticmethod
    def brightness_decrease(wait=0.01, step=1):
        """Decrease the brightness until black"""
        for j in range(int(256 // step)):
            for i in range(LightsController.pixels.count()):
                r, g, b = LightsController.pixels.get_pixel_rgb(i)
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                # we don't need to check the is_rbg flag here because this decreases from the current values
                LightsController.pixels.set_pixel_rgb(i, r, g, b)
            LightsController.pixels.show()
            # if we have reached black, then we are done
            if r == 0 and g == 0 and b == 0:
                break
            if wait > 0:
                time.sleep(wait)

    @staticmethod
    def brightness_increase(wait=0.01, step=1):
        """Increase the brightness until full"""
        for j in range(int(256 // step)):
            for i in range(LightsController.pixels.count()):
                r = int(min(j, config.color['r']))
                g = int(min(j, config.color['g']))
                b = int(min(j, config.color['b']))
                if config.is_rbg:
                    LightsController.pixels.set_pixel_rgb(i, r, b, g)
                else:
                    LightsController.pixels.set_pixel_rgb(i, r, g, b)
            LightsController.pixels.show()
            # if we have reached the full color, then we are done
            if r == config.color['r'] and g == config.color['g'] and b == config.color['b']:
                break
            if wait > 0:
                time.sleep(wait)
    
    @staticmethod
    def wheel(pos):
        """The wheel function to interpolate between different hues"""
        if pos < 85:
            return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)

    @staticmethod
    def start_pattern(pattern='fill_up', delay=0.1, pause=0.5, rounds=0):
        """Start a running pattern.  This is done by forking a new process to 
           run the pattern so that it will run indefinitely.
           There can only be one forked process at a time.
        """
        LightsController.stop_existing_process()
        LightsController.process = Process(target=globals()[pattern], args=(delay, pause, rounds))
        LightsController.process.start()
    
    @staticmethod
    def stop_existing_process():
        """Stop an existing process if there is one
           Running through uwsgi it seems that SIGKILL is necessary as
           .terminate() did not work.  It seems the process ignores the SIGTERM signal.
        """
        if LightsController.process is not None and LightsController.process.is_alive():
            #LightsController.process.terminate()
            try:
                os.kill(LightsController.process.pid, signal.SIGKILL)
                # wait for the process in order to reap it (avoids having defunct zombie processes leftover)
                os.waitpid(LightsController.process.pid, 0)
            except OSError:
                pass
            except Exception as e:
                logging.exception('Error in stop_existing_process')
    
# Define all light patterns
# Each pattern function should take three parameters:
#   delay - lengh of the delay used in the pattern
#   pause - length of the pause used in the pattern (i.e. in between rounds)
#   rounds - the number of rounds to do before finishing
#
# A pattern should run indefinitely if the number of rounds is 0.

def all_random(delay=0, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        # get random pattern
        pattern = random.sample(patterns, 1)[0]
        # get random values
        pattern_delay = random.uniform(0.005, 0.05)
        pattern_pause = random.uniform(0.5, 5)
        pattern_rounds = random.randint(3, 6)
        logging.debug("Doing %s delay %s pause %s rounds %d", pattern, str(pattern_delay), str(pattern_pause), pattern_rounds)
        globals()[pattern](pattern_delay, pattern_pause, pattern_rounds)
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True
    
def chase_up(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
            LightsController.off([light], stop_existing=False)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True
        
def chase_down(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights[::-1]:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
            LightsController.off([light], stop_existing=False)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_up(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        LightsController.off(stop_existing=False)
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_down(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights[::-1]:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        LightsController.off(stop_existing=False)
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fill_up_and_down(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        for light in pattern_lights[::-1]:
            LightsController.off([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True
                
def fill_up_chase_up(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for light in pattern_lights:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
        for light in pattern_lights:
            LightsController.off([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        LightsController.off(stop_existing=False)
        time.sleep(delay)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def alternating(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    group1 = [i for i in pattern_lights if i % 2]
    group2 = [i for i in pattern_lights if i % 2 == 0]
    while not done:
        LightsController.off(group2, stop_existing=False)
        time.sleep(delay)
        LightsController.on(group1, stop_existing=False)
        time.sleep(pause)
        LightsController.on(group2, stop_existing=False)
        time.sleep(delay)
        LightsController.off(group1, stop_existing=False)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def random_sets(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        # get a random half from the available lights
        lights = random.sample(pattern_lights, config.pixel_count / 2)
        LightsController.on(lights, stop_existing=False)
        time.sleep(pause)
        LightsController.off(lights, stop_existing=False)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def random_on_off(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    lights = pattern_lights
    while not done:
        random.shuffle(lights)
        for light in lights:
            LightsController.on([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        random.shuffle(lights)
        for light in lights:
            LightsController.off([light], stop_existing=False)
            time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def appear_from_back(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        # in order to speed up this pattern in goes in "blocks" of 10
        for i in range(0, config.pixel_count, 10):
            for j in reversed(range(i, config.pixel_count)):
                LightsController.pixels.clear()
                # first set all pixels at the beginning
                for k in range(i):
                    LightsController.set_color(k, show=False)
                # set the pixel at position j and the 9 preceeding pixels
                for m in range(max(j-9, 0), j+1):
                    LightsController.set_color(m, show=False)
                LightsController.pixels.show()
                time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def fade_in_out(delay=0.1, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        LightsController.brightness_increase(wait=delay)
        time.sleep(pause)
        LightsController.brightness_decrease(wait=delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def rainbow_cycle(delay=0.005, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in pattern_lights:
                LightsController.pixels.set_pixel(i, LightsController.wheel(((i * 256 // LightsController.pixels.count()) + j) % 256) )
            LightsController.pixels.show()
            if delay > 0:
                time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True

def rainbow_colors(delay=0.05, pause=0.5, rounds=0):
    LightsController.off(stop_existing=False)
    done = False
    current_round = rounds
    while not done:
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in pattern_lights:
                LightsController.pixels.set_pixel(i, LightsController.wheel(((256 // LightsController.pixels.count() + j)) % 256) )
            LightsController.pixels.show()
            if delay > 0:
                time.sleep(delay)
        time.sleep(pause)
        if rounds > 0:
            current_round -= 1
            if current_round <= 0:
                done = True