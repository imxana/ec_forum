from flask import Flask, request, url_for

app = Flask(__name__)

import ec_forum.account as ac
import ec_forum.salt as salt
import ec_forum.userinfo as uinfo
import ec_forum.article as article
# import ec.forum.question as question

ac.run(app)
salt.run(app)
uinfo.run(app)
article.run(app)
# question.run(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
