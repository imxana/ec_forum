database

sy_user

字段 | 字段 | 备注
-|-|-
u_id | 用户id | int 主键
u_name | 用户名 | str 必填唯一
u_email | 用户email | str 必填
u_email_confirm | 用户email是否验证 | int
u_level | 用户权限等级 | int
u_reputation | 用户声望 | int
u_realname | 用户真实姓名 | str，非必填

sy_question

字段 | 字段 | 备注
-|-|-
q_id | 问题id | int 主键
u_id | 提问用户id | int 外键
q_title | 问题标题 | str 非空
q_text | 问题正文 | str 非空
q_date | 提问日期 | date 

sy_answer

字段 | 字段 | 备注
-|-|-
a_id | 回答id | int 主键
u_id | 回答用户id | int 外键
a_text | 回答正文 | str 非空
a_date | 回答日期 | date 
a_reputation | 回答获得声望 | int

sy_article

字段 | 字段 | 备注
-|-|-
t_id | 文章id | int 主键
u_id | 文章作者id | int 外键
t_title | 文章标题 | str 非空
t_text | 文章正文 | str 非空
t_date | 文章发表日期 | date 
t_reputation | 文章获得声望 | int

sy_comment

字段 | 字段 | 备注
-|-|-
c_id | 评论id | int 主键
t_id | 文章id | int 外键
u_id | 评论用户id | int 外键
c_text | 评论正文 | str 非空
a_date | 评论日期 | date 

sy_reputaion

