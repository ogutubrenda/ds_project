from flask import Flask, jsonify, os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Hello from Server!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
