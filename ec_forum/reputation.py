from ec_forum.sql import sqlQ
sqlQ = sqlQ()

event = {
    'email_confirm_pass'           : [ +1 ],
    'article_add'                  : [ 0 ],
    'article_recommend'            : [ 0, +1 ],
    'article_star'                 : [ 0, +1 ],
    'article_del_other'            : [-1, -1 ],
    'comment_add'                  : [ 0,  0 ],
    'comment_like'                 : [ 0,  0 ],
    'comment_dislike'              : [ 0,  0 ],
    'question_add'                 : [ +1 ],
    'question_like'                : [ 0, +5 ],
    'question_dislike'             : [ 0, -2 ],
    'question_star'                : [ 0, +1 ],
    'answer_add'                   : [+1, +1 ],
    'answer_star'                  : [ 0, +1 ],
    'answer_like'                  : [ 0, +10],
    'answer_dislike'               : [-1, -2 ],
}



rule = {
    'comment_like'                 :    1,
    'report'                       :   15,
    'answer_like'                  :   15,
    'question_like'                :   15,
    'article_like'                 :   15,
    'tag_edit'                     :  100,
    'answer_dislike'               :  125,
    'question_dislike'             :  125,
    'question_edit'                :  200,
    'answer_edit'                  :  200,
    'question_close'               : 1000,
    'tag_new'                      : 1500,
    'answer_delete'                : 3000,
    'question_delete'              : 5000,
}


def event_translator(r_type,ec_type,ec_id,u_id,ua_id,ua_rep,ub_id,ub_rep):
    err,res = sqlQ.id_select(ec_id, table='ec_'+ec_type)
    err,ua = sqlQ.id_select(ua_id,'ec_user')
    err,ub = sqlQ.id_select(ub_id,'ec_user')
    ch = {'article':'文章','question':'问题','answer':'回答'}
    def sc(text):
        if len(text)>=30:
            text = text[:28]+'...'
        return text
    if r_type == 'email_confirm_pass':
        return ua_rep, '邮箱 %s 验证通过'%res[3]
    elif r_type == 'article_add':
        return ua_rep, '添加了文章 *%s*'%res[2]
    elif r_type == 'comment_add':
        title = sc(res[2])
        if ec_type == 'answer':
            title = ''
        if u_id == ua_id:
            return ua_rep, '评论了用户%s的%s%s'%(ub[1],ch[ec_type],' *'+title+'* ')
        else:
            return ub_rep, '您的%s%s被用户%s评论了'%(ch[ec_type],' *'+title+'* ',ua[1])
    elif r_type == 'article_star':
        title = sc(res[2])
        if u_id == ua_id:
            return ua_rep, '收藏了%s的文章 *%s*'%(ub[1],title)
        else:
            return ub_rep, '您的文章 *%s* 被用户%s收藏了'%(title,ua[1])
    elif r_type == 'article_recommend':
        title = sc(res[2])
        if u_id == ua_id:
            return ua_rep, '推荐了%s的文章 *%s*'%(ub[1],title)
        else:
            return ub_rep, '您的文章 *%s* 被用户%s推荐了'%(title,ua[1])



