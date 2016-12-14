from flask import request, jsonify
import ec_forum.error as error
from ec_forum.sql import sqlQ

sqlQ = sqlQ()

qiniu_setting = {
    'access_key' : 'iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im',
    'secret_key' : 'AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A',
    'bucket_name' : 'image',
    'bucket_domain' : 'https://oi3qt7c8d.qnssl.com/',
    'callbakUrl' : 'http://139.129.24.151/image/upload',
    'callbackBody' : 'filename:$(fname)&filesize:$(fsize)'
}

def run(app):

    @app.route('/image/upload', methods=['POST'])
    def image_upload():
        """
        'callbackBody':'filename=$(fname)&filesize=$(fsize)'
        """
        i_name = request.values.get('filename', '')
        # i_size = request.values.get('filesize', '')
        if i_name == '':
            return jsonify(error.argsEmpty)
        i_url = qiniu_setting['bucket_domain'] + i_name
        err,i_id = sqlQ.image_insert(i_url)
        if err:
            return jsonify(error.serverError)
     
        return jsonify({
            'code': '1',
            'i_id': i_id,
            'i_url': i_url
            })



    @app.route('/image/query', methods=['GET'])
    def image_query():
        i_id = request.args.get('i_id', '')
        
        'empty'
        if i_id == '':
            return jsonify(error.imageidEmpty)

        err, res = sqlQ.id_search(i_id, table='ec_image')
        if err:
            return jsonify(error.imageNotExisted)

        return jsonify({
            'code':'1', 
            'i_id':res[0],
            'i_url':res[1]
            })




