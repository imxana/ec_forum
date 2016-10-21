from flask import request,jsonify
import ec_forum.error as error
import ec_forum.expr as expr
from ec_forum.sql import sqlQ
from ec_forum.salt import encrypt, decrypt, secret_key
from ec_forum.id_dealer import pack_id, unpack_id
from ec_forum.public import default_tags

sqlQ = sqlQ()

def run(app):

    @app.route('/')
