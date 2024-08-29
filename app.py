from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from handlers.relay_handler import move_down, move_left, move_up, move_right, stop
from handlers.elevation_handler import ElevationHandler
from handlers.rotation_handler import RotationHandler
import time

app = Flask(__name__)
socketio = SocketIO(app)

elevation_handler = ElevationHandler()
elevation_handler.start()
rotation_handler = RotationHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_angles')
def get_angles():
    elevation = elevation_handler.get_last_printed_angle()
    azimuth_angle = angle_handler.get_angle()
    return jsonify({'elevation': elevation, 'azimuth': f'{round(azimuth_angle)}d'})

@socketio.on('button_event')
def handle_button_event(data):
    button_name = data.get('button_name')
    action = data.get('action')

    if action == 'press':
        if button_name in ['left', 'right']:
            rotation_handler.start_tracking(button_name)
            if button_name == 'up':
                move_up()
            elif button_name == 'down':
                move_down()
            elif button_name == 'left':
                move_left()
            elif button_name == 'right':
                move_right()

    elif action == 'release':
        if button_name in ['left', 'right']:
            rotation_handler.stop_tracking()
        stop()

    # Emit the updated angle to all connected clients
    emit('angle_update', {'azimuth': round(angle_handler.get_angle())})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
