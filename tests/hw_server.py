from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def hw():
    return jsonify({1:set(2,3)})


if __name__ == '__main__':
    app.run()
