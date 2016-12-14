import flask
from ec_forum.sql import sqlQ

sqlQ = sqlQ()


def run(app):

    @app.route('/image/upload', method=['POST'])
    def image_upload():
        i_name = request.values.get('filename', '')
        # i_size = request.values.get('filesize', '')         
        bucket_domain = 'http://oi3qt7c8d.qnssl.com/'
        i_url = '%s'
     
        return jsonify({'code': '1'})


    @app.route('/image/query', method=['GET'])
    def image_query():
        i_id = request.args.get('i_id', '')
        
        'empty'
        if i_id == '':
            return 'no'

        'exist'


        return jsonify({'code': '1'})
