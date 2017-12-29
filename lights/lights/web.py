# Lights web interface
# Phil Hansen, 22 October 2016
# Copyright Notice

from flask import Flask, g, render_template, request
import config

try:
    from lights import LightsController, patterns
except RuntimeError:
    # a RuntimeError occurs when the GPIO interface could not be loaded
    # (e.g. if not running on a Raspberry Pi)
    # in this case load the mock version of the controller
    from lights_mock import LightsController, patterns

# set key for sessions
SECRET_KEY = 'HDRE%(@3278skdfdD34@^*'
app = Flask(__name__, template_folder=config.path_templates, static_folder=config.path_web, static_url_path='/static')
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.title = config.title
    # format the RGB color value as the 6 character hex code
    g.color = get_color_in_hex()
    # only need to do this once
    if not config.initialized:
        LightsController.setup()
        config.initialized = True
    
@app.route('/')
def index():
    """Main page"""
    display = {}
    # format pattern for display
    for pattern in patterns:
        display[pattern] = pattern.replace('_', ' ').title()
    return render_template('index.html', patterns=patterns, display=display)

@app.route('/lights/on', methods=['GET', 'POST'])
@app.route('/lights/on/', methods=['GET', 'POST'])
@app.route('/lights/on/<id>', methods=['GET', 'POST'])
def lights_on(id=None):
    """Turn lights on, either a specific ID or all lights"""
    if id is None:
        LightsController.on()
    else:
        LightsController.on([int(id)])
    return ''
    
@app.route('/lights/off', methods=['GET', 'POST'])
@app.route('/lights/off/', methods=['GET', 'POST'])
@app.route('/lights/off/<id>', methods=['GET', 'POST'])
def lights_off(id=None):
    """Turn lights off, either a specific ID or all lights"""
    if id is None:
        LightsController.off()
    else:
        LightsController.off([int(id)])
    return ''

@app.route('/lights/color', methods=['GET', 'POST'])
@app.route('/lights/color/', methods=['GET', 'POST'])
def lights_color():
    """Set color of lights
       A color value can be posted by specifying (r, g, b) in JSON
    """
    try:
        data = request.get_json(force=True)
        if data is not None and 'r' in data:
            config.color = data
            LightsController.set_color()
    except Exception:
        pass
    return ''

@app.route('/lights/random_color', methods=['GET', 'POST'])
@app.route('/lights/random_color/', methods=['GET', 'POST'])
def lights_random_color():
    """Set color of lights to a random color
       Returns the color value in hex in order to update the color picker
    """
    config.color = LightsController.get_random_color()
    LightsController.set_color()
    return get_color_in_hex()

def get_color_in_hex():
    """Returns the RGB color value formatted as a 6 character hex code"""
    return '#%02x%02x%02x' % (config.color['r'], config.color['g'], config.color['b'])
    
@app.route('/lights/slide/bottom/<value>', methods=['GET', 'POST'])
def lights_bottom_to_top(value):
    """Turn all lights on up to value, from bottom to top"""
    if value == '-1':
        LightsController.off()
    else:
        lights = []
        current = 0
        while current <= int(value):
            lights.append(current)
            current += 1
        LightsController.on(lights)
        LightsController.off(list(set(range(0, config.pixel_count)) - set(lights)))
    return ''

@app.route('/lights/slide/top/<value>', methods=['GET', 'POST'])
def lights_top_to_bottom(value):
    """Turn all lights on up to value, from top to bottom"""
    if value == config.pixel_count:
        LightsController.off()
    else:
        lights = []
        current = config.pixel_count - 1
        while current >= int(value):
            lights.append(current)
            current -= 1
        LightsController.on(lights)
        LightsController.off(list(set(range(0, config.pixel_count)) - set(lights)))
    return ''

@app.route('/lights/pattern', methods=['GET', 'POST'])
def pattern():
    """Start a pattern
       Expected arguments are: name, delay, pause
    """
    if request.args.get('name') is None:
        return ''
    pattern = request.args.get('name')
    delay = float(request.args.get('delay', 0.1))
    pause = float(request.args.get('pause', 0.5))
    LightsController.start_pattern(pattern=pattern, delay=delay, pause=pause)
    return ''
    
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
        )
