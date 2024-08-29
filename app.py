from flask import Flask, render_template, jsonify, request
from handlers.relay_handler import move_down, move_left, move_up, move_right, stop, correct_elevation
from handlers.elevation_handler import ElevationHandler
import time
# from handlers.azimuth_handler import RotaryEncoderHandler

app = Flask(__name__)

elevation_handler = ElevationHandler()
elevation_handler.start()

# azimuth_handler = RotaryEncoderHandler()
# azimuth_handler.start()

saved_elevation_angle = None

@app.route('/')

def index():
    return render_template('index.html')

@app.route('/get_angles')
def get_angles():
    elevation = elevation_handler.get_last_printed_angle()
    # azimuth = elevation_handler.get_angle()
    return jsonify({'elevation': elevation, 'azimuth': '30d'})

@app.route('/button_event', methods=['POST'])
def button_event():
    global button_message
    global saved_elevation_angle
    button_name = request.json.get('button_name')
    action = request.json.get('action')
    current_angle = elevation_handler.get_last_printed_angle()

    if action == 'press':
        if button_name == 'up':
            move_up()
        elif button_name == 'down':
            move_down()
        elif button_name == 'left' or button_name == 'right':
            # Save the current elevation angle before rotating
            # saved_elevation_angle = current_angle
            if button_name == 'left':
                move_left()
            elif button_name == 'right':
                move_right()
    elif action == 'release':
        stop()
        # time.sleep(0.1)
        # if button_name == 'left' or button_name == 'right':
        #     #Correct the elevation after rotating
        #     correct_elevation(saved_elevation_angle, current_angle)

    return jsonify({'button_message': 'test'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

