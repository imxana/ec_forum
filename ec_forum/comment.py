from flask import request,jsonify
import ec_forum.error as error
import ec_forum.sql as sql
import ec_forum.expr as expr
from ec_forum.salt import encrypt, decrypt
from ec_forum.id_dealer import pack_id, unpack_id

def run(app):

    @app.route('/c/add', methods=['POST'])
    def coment_add():
        return 'fuck'

    @app.route('/c/del', methods=['POST'])
    def coment_del():
        return 'fuck'
    
    @app.route('/c/l', methods=['POST'])
    def coment_l():
        return 'fuck'
