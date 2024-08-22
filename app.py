from flask import Flask, render_template, jsonify, request
from handlers.relay_handler import move_down, move_left, move_up, move_right, stop

app = Flask(__name__)

value1 = "30d"
value2 = "30d"

@app.route('/')
def index():
    return render_template('index.html', value1=value1, value2=value2)

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

