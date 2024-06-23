#Contains the code for the simple web server with the /home and /heartbeat endpoints. (TASK  1)
from flask import Flask

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    # Replace 'WORKING SERVER' with a unique identifier
    return 'Hello from WORKING SERVER'

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)