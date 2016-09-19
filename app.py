from flask import Flask, request, url_for

app = Flask(__name__)

import ec_forum.account as ac
import ec_forum.salt as salt

ac.run(app)
salt.run(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

