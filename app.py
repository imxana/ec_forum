from flask import Flask, request, url_for
import config

app = Flask(__name__)

# config_mode = ['TestingConfig','DevelopmentConfig','ProductionConfig']
# app.config.from_object('config.'+config_mode[0])

import ec_forum.account as ac
import ec_forum.salt as salt
import ec_forum.userinfo as uinfo
import ec_forum.article as article
import ec_forum.public as public
import ec_forum.comment as comment
# import ec.forum.question as question


ac.run(app)
salt.run(app)
uinfo.run(app)
article.run(app)
public.run(app)
comment.run(app)
# question.run(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
