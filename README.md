# led-lights

This project is for controlling an LED light strip (WS2801) running on a Raspberry Pi.  Everything runs in a Docker container.  
The project includes two Dockerfiles and associated files.  One is for running on the Raspberry Pi itself, and the other 
is for running on a regular x86 machine for testing and development purposes.  There are two scripts in the root of the 
project that are used for building andd running the Docker image/container.  The scripts will automatically use the correct 
Dockerfile depending on the machine architecture.  On your Raspberry Pi all you need to do is install Docker before using 
the below scripts.

To build the image run: ```./build```

To run the container run: ```./run```

Optionally you can set the port using the ```-p``` flag, or use ```-c``` to run the container and start at the bash terminal.
This can be useful for testing or development purposes.

The Docker container runs a simple web app which is how the LED lights are controlled.  Simply browse to the IP address of your 
Raspberry Pi to control the lights.  The color of the lights can be selected and there are various patterns.  When selecting 
a pattern it will run indefinitely until the next pattern is chosen.  There is an "All" button which will randomly run each 
pattern with randomized parameters (delay, pause, and number of rounds).

The WS2801 library from Adafruit is used to control the LEDs.

## Config file

The config file in the project, ```config.ini-dist```, should be copied to ```config.ini```.  This allows you to configure a few 
things like the total number of pixels and the log level.  There is also an ```is_rbg``` flag which you can use to designate that your 
LED strip is actually RBG and not RGB (as I found out with my own LED strip).  If this flag is enabled it simply swaps the blue and 
green values when setting colors.

## Project layout

```
docker - Dockerfile and associated files for running on the Raspberry Pi
docker_x86 - Dockerfile and associated files for running on an x86 machine
lights - The python web app
    Adafruit_WS2801 - python library to control WS2801 LED lights (included locally because it uses a forked version)
    lights - python web app
    templates - HTML templates
    var - var data (e.g. log file)
    web - static web files (e.g. css/js files)
```

## Third party libraries added to the project

Adafruit_WS2801 - python library to control WS2801 LED lights
    * Downloaded a fork with a bug fix from https://github.com/HeMan/Adafruit_Python_WS2801

Bootstrap - https://getbootstrap.com/

jQuery - http://jquery.com/

jQuery MiniColors Plugin - https://github.com/claviska/jquery-minicolors

rangeslider.js - https://github.com/andreruffert/rangeslider.js
