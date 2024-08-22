from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

value1 = "Значення 1"
value2 = "Значення 2"
button_message = ""  

@app.route('/')
def index():
    return render_template('index.html', value1=value1, value2=value2, button_message=button_message)

@app.route('/button_event', methods=['POST'])
def button_event():
    global button_message
    button_name = request.json.get('button_name')
    action = request.json.get('action')

    if action == 'press':
        button_message = f"Кнопка {button_name} натиснута"
    elif action == 'release':
        button_message = ""

    return jsonify({'button_message': button_message})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

