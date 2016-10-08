import os, sys
import smtplib
from flask import jsonify
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from ec_forum.id_dealer import gene_id
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
        return jsonify({'code':'1','tags':default_tags})

    @app.route('/public/get_verify')
    def get_verify():
        return jsonify({'code':'1','verify':gene_id(num=5,letter=True).upper()})


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
    print(52)
    smtp = SMTP_SSL(mailInfo["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mailInfo["hostname"])
    smtp.login(mailInfo["username"],mailInfo["password"])
    print(57)

    #msg = MIMEText(mailInfo["mailtext"],"text",mailInfo["mailencoding"])
    msg = MIMEText(mailInfo["mailtext"])
    msg["Subject"] = Header(mailInfo["mailsubject"],mailInfo["mailencoding"])
    msg["from"] = mailInfo["from"]
    msg["to"] = mailInfo["to"]
    smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())
    print(65)
    smtp.quit()
