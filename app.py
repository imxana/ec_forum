from flask import Flask, request, url_for

app = Flask(__name__)

import ec_forum.account as ac



if __name__ == '__main__':
    app.run(host='0.0.0.0')

