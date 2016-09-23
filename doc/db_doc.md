database

## 这张表已经被废弃了！废弃了！废弃了！以 ./doc/schema.sql 为准！

## ec_user

字段 | 字段 | 备注
------------ | ------------- | ------------
u_id | 用户id | int 主键
u_name | 用户名 | str 必填唯一
u_psw text,
u_email | 用户email | str 必填
u_email_confirm | 用户email是否验证 | int
u_level | 用户权限等级 | int
u_reputation | 用户声望 | int
u_realname | 用户真实姓名 | str，非必填
u_blog text,
u_github text,
u_articles text,
u_questions text,
u_answers text,

## ec_question

字段 | 字段 | 备注
------------ | ------------- | ------------
q_id | 问题id | int 主键
u_id | 提问用户id | int 外键
q_title | 问题标题 | str 非空
q_tag | 问题标签 | str
q_text | 问题正文 | str 非空
q_date | 提问日期 | date
q_close | 是否关闭 | int
q_report | 被举报次数 | int

## ec_answer

字段 | 字段 | 备注
------------ | ------------- | ------------
a_id | 回答id | int 主键
u_id | 回答用户id | int 外键
a_text | 回答正文 | str 非空
a_date | 回答日期 | date
a_like | 回答被赞数 | int

## ec_article

字段 | 字段 | 备注
------------ | ------------- | ------------
t_id | 文章id | int 主键
u_id | 文章作者id | int 外键
t_title | 文章标题 | str 非空
t_text | 文章正文 | str 非空
t_date | 文章发表日期 | date
t_reputation | 文章获得声望 | int

## ec_comment

字段 | 字段 | 备注
------------ | ------------- | ------------
c_id | 评论id | int 主键
type | 评论类型 | q/a/t
id | 对应事件id | int 外键
u_id | 评论用户id | int 外键
c_text | 评论正文 | str 非空
c_date | 评论日期 | date
c_like | 评论被赞数 | int

## ec_reputaion

字段 | 字段 | 备注
------------ | ------------- | ------------
r_id | 声望变化id | 主键
type | 声望类型 | q/a/t/c
id | 对应事件id | int 外键
ua_id | 评价用户id | int 外键
ub_id | 接受用户id | int 外键
