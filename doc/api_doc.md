# Public

## 获取所有基础tag ./public/tags

method:get

return: array

## 获取5位随机验证码 ./public/get_verify

method:get

return: str

## 获取密钥 ./safe/secret_key (之后将隐藏此API)

method:get

return: str

# Acount

## 注册 ./sign_up

method:post

字段|类型|要求
------------ | ------------- | ------------
u_email| str|[A-Za-z0-9\_\.]+@[A-Za-z0-9\.]+\.[A-Za-z]{2,4}
u_name| str|[a-z][a-z0-9\.]{2,20}
u_psw| str|6<=len(psw)<=16


suc:

字段|类型或值
------------ | -------------
code|1
u_id|int


fail:

字段|类型或值
------------ | -------------
code|!1
codeState| str


## 登录 ./sign_in

method:post

字段|类型
------------ | -------------
u_loginname(u_name/u_email)| str
u_psw| str

suc:

字段|类型或值
------------ | -------------
code|1
u_id|int
u_name|str
u_email | str
u_email_confirm | int
u_level |  int
u_reputation |  int
u_realname | str
u_blog | str
u_github | str
u_articles | str
u_questions | str
u_answers | str
u_watchusers | str
u_tags | str
u_intro | str


fail:

字段|类型或值
------------ | -------------
code|!1
codeState| str


## 删除用户（仅测试用） ./safe/sign_del

method:post

字段|类型
------------ | -------------
u_name/u_email| str
u_psw| str


suc:

字段|类型或值
------------ | -------------
code|1


fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str


# User_info

## 查询用户信息 ./u/query

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填

suc:

字段|类型或值
------------ | -------------
code|1
u_id|int
u_name|str
u_email | str
u_level |  int
u_reputation |  int
u_realname | str
u_blog | str
u_github | str
u_articles | str
u_questions | str
u_answers | str
u_watchusers | str
u_tags | str
u_intro | str



fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 更新用户信息 ./u/update

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证
u_realname | str | 无要求
u_blog | str | 无要求
u_github | str | 无要求
u_tags | str | ','分割
u_intro | str | 无要求

suc:

字段|类型或值
------------ | -------------
code|1


fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 关注用户 ./u/follow

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | -
u_psw | str | -
ua_id | int | -
u_act | int | 1关注 0取关

suc:

字段|类型或值
------------ | -------------
code|1


fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str


## 发送验证邮箱邮件 ./u/email/verify

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_email| str | 必填
u_verify | str| 必填

suc:

字段|类型或值
------------ | -------------
code|1



## 邮箱验证通过 ./u/email/confirm

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw| str | 必填

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str




## 修改用户邮箱 ./u/email/change

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw| str | 必填
u_email| str | 必填

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 根据旧密码修改用户密码 ./u/psw/change

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw_before| str | 必填，旧密码
u_psw| str | 必填，新密码

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 发送修改密码验证邮件 ./u/psw/verify

method:post

字段|类型|要求
------------ | ------------- | ------------
u_loginname | str | 必填
u_verify | str | 必填

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 重设用户密码 ./u/psw/reset

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw| str | 必填，新密码

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 查询声望记录 ./u/rep/history

要求：查询记录时会更新个人声望值，希望界面ui做出反馈，比如 <个人声望已更新>

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证


suc:

字段|类型或值
------------ | -------------
code | 1
history | [^history array]

^history info

字段|类型或值
------------ | -------------
rep | int
action | str
date | int



fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str



# Article

## 添加文章 ./t/add

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证
t_title | str | 非空
t_text | str | 非空
t_tags | str | 无要求


suc:

字段|类型或值
------------ | -------------
code | 1
t_id | int


fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## 更新文章 ./t/update

method:post

字段|类型
------------ | -------------
u_id | int
u_psw | str
t_id | int
t_title| str
t_text| str
t_tags| str

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 删除文章 ./t/del

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
t_id | int


suc:

字段|类型或值
------------ | -------------
code|1
t_id | int

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str


## 获取展示文章列表 ./t/display


method:post

字段|类型
------------ | -------------
t_tags | str ex:'python,nodejs'
show_count | 可选,默认30

suc:

字段|类型
------------ | -------------
code | 1
t_ids | str 'by,hot&by,time'

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 查询文章信息 ./t/query

method:post

字段|类型
------------ | -------------
t_id | int

suc:

字段|类型或值
------------ | -------------
code | 1
t_id | int
u_id | int
t_title | str
t_text | str
t_date | int
t_like | str
t_comments | str
t_tags | str
t_date_latest | int
t_star | str

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 查询文章信息 ./t/query_pro

method:post

字段|类型
------------ | -------------
t_id | int
u_id | int
u_psw | str

suc:

字段|类型或值
------------ | -------------
code | 1
t_star_bool | 1/0
t_recommend_bool | 1/0

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 收藏文章 ./t/star


method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
t_id | int
u_act | str(1表示收藏,0表示取消收藏)

suc:

字段|类型或值
------------ | -------------
code | 1
r_id | int(如果u_act=='0'则无此参数)

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 静默移除失效文章 ./t/star_unlink

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
t_id | int

suc:

字段|类型或值
------------ | -------------
code | 1

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 推荐文章 ./t/recommend


method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
t_id | int
u_act | str(1表示推荐,0表示取消推荐)

suc:

字段|类型或值
------------ | -------------
code | 1
r_id | int(如果u_act=='0'则无此参数)

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

# Comment

## 发表评论 ./c/add

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证
ec_type | str | article/question/answer
ec_id | int | 必填
c_text | str | 非空

suc:

字段|类型或值
------------ | -------------
code | 1
c_id | int

fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str


## 删除评论 ./c/del

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
c_id | int


suc:

字段|类型或值
------------ | -------------
code|1
c_id | int

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 查询评论信息 ./c/query

method:post

字段|类型
------------ | -------------
c_id | int

suc:

字段|类型或值
------------ | -------------
code | 1
c_id | int
u_id | int
ec_type | article/question/answer
ec_id | int
c_date | int
c_like | str


fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str


# Question

## 添加问题 ./q/add

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证
q_title | str | 非空
q_text | str | 非空
q_tags | str | 无要求


suc:

字段|类型或值
------------ | -------------
code | 1
q_id | int


fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str


## 更新问题信息./q/update

method:post

字段|类型
------------ | -------------
u_id | int
u_psw | str
q_id | int
q_title| str
q_text| str
q_tags| str

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 删除文章 ./q/del

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
q_id | int


suc:

字段|类型或值
------------ | -------------
code|1
q_id | int

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str


## 获取问题展示列表 ./q/display


method:post

字段|类型
------------ | -------------
q_tags | str ex:'python,nodejs'
show_count | 可选,默认30

suc:

字段|类型
------------ | -------------
code | 1
t_ids | str ex:'by,hot&by,time'

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 查询问题信息 ./q/query

method:post

字段|类型
------------ | -------------
q_id | int

suc:

字段|类型或值
------------ | -------------
code | 1
q_id | int
u_id | int
q_title | str
q_tags | str
q_text | str
q_date | int
q_like | str
q_close | int
q_report | int
q_answers | str
q_comments | str
q_date_latest | int
q_star | str

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str


## 查询问题信息UI ./q/query_pro

method:post

字段|类型
------------ | -------------
q_id | int
u_id | int
u_psw | str

suc:

字段|类型或值
------------ | -------------
code | 1
q_star_bool | 1/0
q_like_state | 1/0/-1

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 收藏问题 ./q/star


method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
q_id | int
u_act | str(1表示收藏,0表示取消收藏)

suc:

字段|类型或值
------------ | -------------
code | 1
r_id | int(如果u_act=='0'则无此参数)

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 静默移除失效收藏问题 ./q/star_unlink

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
q_id | int

suc:

字段|类型或值
------------ | -------------
code | 1

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## 赞同问题 ./q/like


method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
q_id | int
u_act | str(1表示赞同,0表示取消赞同或反对,-1表示反对)

suc:

字段|类型或值
------------ | -------------
code | 1
r_id | int(如果u_act=='0'则无此参数)
message | str(u_act=='0'时的消息，显示变化情况)

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str


# Answer

## ./a/add
## ./a/query
## ./a/update
## ./a/del
## ./a/query
## ./a/query_pro
## ./a/star
## ./a/star_unlink
## ./a/like


