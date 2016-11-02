create database ec_forum;

use ec_forum;

create table ec_user
(
    u_id integer primary key comment '用户ID',
    u_name text comment '用户名',
    u_psw text comment '密码',
    u_email text comment '用户email',
    u_email_confirm integer comment '用户email是否验证',
    u_level integer comment '用户权限等级',
    u_reputation integer comment '用户声望',
    u_realname text comment '真实姓名',
    u_blog text comment '博客地址',
    u_github text comment 'github地址',
    u_articles text comment '文章ID组，我的文章和收藏文章',
    u_questions text comment '提问ID组，我的提问和收藏问题',
    u_answers text comment '回答ID组，我的回答和收藏回答',
    u_watchusers text comment '关注用户ID组',
    u_tags text comment '关注标签',
    u_intro text comment '个人签名',
    u_img text comment '用户头像链接'
);

create table ec_question
(
    q_id integer comment '问题id',
    u_id integer comment '提问用户id',
    q_title text comment '问题标题',
    q_tags text comment '问题标签',
    q_text text comment '问题正文',
    q_date datetime comment '提问日期',
    q_like integer comment '提问被赞数',
    q_close integer comment '是否关闭',
    q_report integer comment '被举报次数',
    q_answers text comment '回答ID组',
    q_comments text comment '评论ID组',
    q_date_latest datetime comment '最后修改时间',
    q_star integer comment '问题收藏数'
);

create table ec_answer
(
    a_id integer primary key comment '回答id',
    u_id integer comment '回答用户id',
    a_text text comment '回答正文',
    a_date datetime comment '回答日期',
    a_like integer comment '回答被赞数',
    a_comments text comment '评论ID组'
);

create table ec_article
(
    t_id integer primary key comment '文章id',
    u_id integer comment '文章作者id',
    t_title text comment '文章标题',
    t_text text comment '文章正文',
    t_date datetime comment '文章发表日期',
    t_like int comment '推荐文章的用户数',
    t_comments text comment '评论ID组',
    t_tags text comment '文章标签',
    t_date_latest datetime comment '最后修改时间',
    t_star int comment '收藏文章的用户数'
);

create table ec_comment
(
    c_id integer primary key comment '评论id',
    ec_type text comment '评论类型 question/answer/article',
    ec_id integer comment '对应事件id',
    u_id integer comment '评论用户id',
    c_text text comment '评论正文',
    c_date datetime comment '评论日期',
    c_like int comment '评论被赞数'
);

create table ec_reputation
(
    r_id integer primary key comment '声望变化事件id',
    r_type text comment '声望类型',
    ec_type text comment '事件类型',
    ec_id integer comment '对应事件id',
    ua_id integer comment '行为用户id',
    ua_rep integer comment '行为用户声望变化',
    ub_id integer comment '接受用户id',
    ub_rep integer comment '接受用户声望变化',
    r_date datetime comment '事件日期'
);

/* comment '(.*)' */
