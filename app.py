from flask import Flask, request, url_for
from flask_cors import *
import config

app = Flask(__name__)
CORS(app, supports_credentials=True)

# config_mode = ['TestingConfig','DevelopmentConfig','ProductionConfig']
# app.config.from_object('config.'+config_mode[0])

import ec_forum.account as ac
import ec_forum.salt as salt
import ec_forum.userinfo as uinfo
import ec_forum.article as article
import ec_forum.public as public
import ec_forum.comment as comment
import ec_forum.question as question
import ec_forum.answer as answer

ac.run(app)
salt.run(app)
uinfo.run(app)
article.run(app)
public.run(app)
comment.run(app)
question.run(app)
answer.run(app)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
