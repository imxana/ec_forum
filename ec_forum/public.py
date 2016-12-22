import os, sys
import smtplib
from flask import jsonify, request
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from ec_forum.id_dealer import gene_id,pack_id,unpack_id
from ec_forum.sql import sqlQ
import ec_forum.error as error

sqlQ = sqlQ()

default_tags = (
        'ios','objective-c','sqlite','safari','xcode','phonegap','cocoa','javascript','macos','iphone','ipad','swift',
        'java','c','c++','php','perl','python','javascript','c#','ruby','objective-c','go','lua','node.js','erlang','scala','bash','actionscript',
        'html','html5','css','css3','javascript','jquery','json','ajax',
        'javascript','jquery','yui','mootools','node.js','chrome','firefox','firebug','internet-explorer',
        'android','java','eclipse','xml','phonegap','json','webview',
        'php','mysql','apache','nginx','数组','mvc','codeigniter','symfony','zend-framework','composer','laravel',
        '数据库','mysql','sqlite','oracle','sql','nosql','redis','mongodb','memcached','postgresql',
        '.net','c#','asp.net','visual-studio','mvc','microsoft',
        'python','list','django','flask','tornado','web.py','sqlalchemy','virtualenv',
        'ruby','ruby-on-rails','rubygems','rvm','macosx','bundle',
        'vim','emacs','ide','eclipse','xcode','intellij-idea','textmate','sublime-text','visual-studio','git','github','svn','hg',
        '云计算','又拍云存储','七牛云存储','google-app-engine','sina-app-engine','amazon-web-services','百度云','金山云',
        'java','java-ee','jar','spring','hibernate','struts','tomcat','maven','eclipse','intellij-idea',
        '搜索引擎','中文分词','全文检索','lucene','solr','sphinx','analyzer','elasticsearch',
        '新浪微博','人人网','微信','腾讯微博','百度','facebook','twitter',
        'linux','unix','ubuntu','windows-server','centos','负载均衡','缓存','apache','nginx',
        )

# question
# eclipse,node.js



def run(app):
    @app.route('/public/tags')
    def get_public_tags():
        return jsonify(list(set(default_tags)))

    @app.route('/public/get_verify')
    def get_verify():
        return gene_id(num=5,letter=True).upper()

    @app.route('/search')
    def search_all():
        word = request.args.get('word','')
        show_count = int(request.args.get('show_count','30'))
        u_dic,t_dic,q_dic,a_dic = {0:[]},{0:[]},{0:[]},{0:[]}

        'user name search'
        err,res = sqlQ.item_select('u_name',word,'ec_user')
        if err:
            return jsonify(error.serverError)
        for t in res:
            u_dic[0].append(str(t[0]))
        u_dic[0] = u_dic[0][:show_count]
        u_ids = pack_id(u_dic)

        'article title search'
        err,res = sqlQ.item_select('t_title',word,'ec_article')
        if err:
            return jsonify(error.serverError)
        for t in res:
            t_dic[0].append(str(t[0]))
        t_dic[0] = t_dic[0][:show_count]
        t_ids = pack_id(t_dic)
            
        'question title search'    
        err,res = sqlQ.item_select('q_title',word,'ec_question')
        if err:
            return jsonify(error.serverError)
        for t in res:
            q_dic[0].append(str(t[0]))
        q_dic[0] = q_dic[0][:show_count]
        q_ids = pack_id(q_dic)
            
        'answer text search'
        err,res = sqlQ.item_select('a_text',word,'ec_answer')
        if err:
            return jsonify(error.serverError)
        for t in res:
            a_dic[0].append(str(t[0]))
        a_dic[0] = a_dic[0][:show_count]
        a_ids = pack_id(a_dic)
        

        

        return jsonify({
            'code':'1',
            'u_ids':u_ids,
            't_ids':t_ids,
            'q_ids':q_ids,
            'a_ids':a_ids
        })
        


def mail_sender(mail_to, mail_title, mail_subject):

    mailInfo = {
            "from":"imxana@qq.com",
            "to":mail_to,
            "hostname":"smtp.qq.com",
            "username":"imxana@qq.com",
            "password":"jjsaojzdfbohbghf",
            "mailsubject":mail_title,
            "mailtext":mail_subject,
            "mailencoding":"utf-8"
            }
    smtp = SMTP_SSL(mailInfo["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mailInfo["hostname"])
    smtp.login(mailInfo["username"],mailInfo["password"])

    #msg = MIMEText(mailInfo["mailtext"],"text",mailInfo["mailencoding"])
    msg = MIMEText(mailInfo["mailtext"])
    msg["Subject"] = Header(mailInfo["mailsubject"],mailInfo["mailencoding"])
    msg["from"] = mailInfo["from"]
    msg["to"] = mailInfo["to"]
    smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())
    smtp.quit()
