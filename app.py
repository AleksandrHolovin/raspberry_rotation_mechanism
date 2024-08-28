from flask import Flask, render_template, jsonify, request
from handlers.relay_handler import move_down, move_left, move_up, move_right, stop
from handlers.elevation_handler import ElevationHandler
from handlers.azimuth_handler import RotaryEncoderHandler

app = Flask(__name__)

value2 = "30d"

elevation_handler = ElevationHandler()
elevation_handler.start()

azimuth_handler = RotaryEncoderHandler()
azimuth_handler.start()

@app.route('/')

def index():
    return render_template('index.html', value2=value2)

@app.route('/get_angles')
def get_angles():
    elevation = elevation_handler.get_last_printed_angle()
    azimuth = elevation_handler.get_angle()
    return jsonify({'elevation': elevation, 'azimuth': azimuth})

@app.route('/button_event', methods=['POST'])
def button_event():
    global button_message
    button_name = request.json.get('button_name')
    action = request.json.get('action')

    if action == 'press':
        if button_name == 'up':
            move_up()
        elif button_name == 'down':
            move_down()
        elif button_name == 'left':
            move_left()
        elif button_name == 'right':
            move_right()
    elif action == 'release':
        stop()

    return jsonify({'button_message': 'test'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

