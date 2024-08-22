from flask import Flask, render_template, jsonify, request

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
        print(f"Button {button_name} pressed")
    elif action == 'release':
        print(f"Button {button_name} released")

    return jsonify({'button_message': 'test'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

