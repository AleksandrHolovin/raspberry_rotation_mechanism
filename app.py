from flask import Flask, render_template, jsonify, request
from handlers.relay_handler import move_down, move_left, move_up, move_right, stop
from handlers.elevation_handler import ElevationHandler
from handlers.rotation_handler import AngleHandler
import time
import os
import logging

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)

logging.basicConfig(
    filename='logs.txt',
    level=logging.ERROR, 
    # filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

elevation_handler = ElevationHandler()
elevation_handler.start()
angle_handler = AngleHandler()

def reboot_pi():
    os.system('sudo reboot')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_angles')
def get_angles():
    elevation = elevation_handler.get_last_printed_angle()
    azimuth_angle = angle_handler.get_angle()
    return jsonify({'elevation': elevation, 'azimuth': f'{round(azimuth_angle)}'})

@app.route('/button_event', methods=['POST'])
def button_event():
    global angle_handler
    button_name = request.json.get('button_name')
    action = request.json.get('action')
    angle = request.json.get('angle')
    
    if action == 'press':
        if button_name == 'up':
            stop()
            move_up()
        elif button_name == 'down':
            stop()
            move_down()
        elif button_name in ['left', 'right']:
            angle_handler.start_tracking(button_name)
            if button_name == 'left':
                stop()
                move_left()
            elif button_name == 'right':
                stop()
                move_right()
        elif button_name == 'stop':
            stop()
        elif button_name == 'reboot':
            reboot_pi()
        elif button_name == 'reset_rotation':
            angle_handler.reset_angle(angle)
    elif action == 'release':
        if button_name in ['left', 'right']:
            angle_handler.stop_tracking()
        stop()

    return jsonify({'button_message': 'test'})

if __name__ == "__main__":
    app.run(host='192.168.161.42', port=5000)
