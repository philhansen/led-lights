# Config for LED Lights
# Phil Hansen, October 22, 2016
# Copyright Notice

import ConfigParser
import logging
import os.path

version = '0.1'
title = 'LED Lights'
path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

# paths
path_templates = os.path.join(path, 'templates')
path_web = os.path.join(path, 'web')

# load config file
config = ConfigParser.ConfigParser()
config.read(os.path.join(path, '../config.ini'))

# total number of pixels
pixel_count = 160
if config.has_section('general') and config.has_option('general', 'pixel_count'):
    pixel_count = config.getint('general', 'pixel_count')

# set to True to designate that the LED lights are RBG (not RGB)
# this will swap the blue and green values when setting colors
is_rbg = True
if config.has_section('general') and config.has_option('general', 'is_rbg'):
    is_rbg = config.getboolean('general', 'is_rbg')

# starting color
color = {
    'r': 255,
    'g': 0,
    'b': 0
}

# flag designating that the Lights Controller has been initialized
initialized = False

# logging
log_file = os.path.join(path, 'var/log/lights.log')
if not os.path.isfile(log_file):
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    open(log_file, 'a').close()
log_level = logging.DEBUG
if config.has_section('logging') and config.has_option('logging', 'level'):
    log_level = config.get('logging', 'level')
logging.basicConfig(filename=log_file, level=log_level, 
                    format='%(asctime)s - %(levelname)-7s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
