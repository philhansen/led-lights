# Mock object for the lights project for testing
# Phil Hansen, 26 November 2017
# Copyright Notice

import random

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

class LightsController(object):
    """This is an empty mock of the LightsController class which is used
       when not running on a Raspberry Pi (e.g. for testing the web interface).
    """
    
    @staticmethod
    def setup():
        """Setup the interfaces"""
        print("setup called")
        
    @staticmethod
    def off(lights=None):
        """Turn off all lights in the given list
           Default all
        """
        print("off called")
    
    @staticmethod
    def on(lights=None):
        """Turn on all lights in the given list
           Default all
        """
        print("on called")
    
    @staticmethod
    def set_color():
        """Set all leds to the current color"""
        print("set_color called")
    
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
    def start_pattern(pattern='fill_up', delay=0.1, pause=0.5, rounds=0):
        print("start_pattern called: %s" % pattern)
    
    @staticmethod
    def stop_existing_process():
        """Stop an existing process if there is one
           Running through uwsgi it seems that SIGKILL is necessary as
           .terminate() did not work.  It seems the process ignores the SIGTERM signal.
        """
        print("stop_existing_process called")
    