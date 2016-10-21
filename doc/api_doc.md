# Public

## 获取所有基础tag ./public/tags

method:get

return: array

## 获取5位随机验证码 ./public/get_verify

method:get

return: str

## 获取密钥 ./safe/secret_key

method:get

return:

字段|类型或值
------------ | -------------
code|1
secret_key| str

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
u_tags | str | 无要求
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

# 关注用户 ./u/follow

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


## 发送验证邮件 ./u/email/verify

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






## 修改用户密码 ./u/psw_change



# Article

## 添加文章 ./t/add

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证
u_title | str | 非空
u_text | str | 非空
u_tags | str | 无要求


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


## ./q/repution

# Comment

## ./c/add

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


## ./c/del

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
t_id | int

fail:

字段|类型或值
------------ | -------------
code | !1
codeState | str

## ./c/query

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

## ./q/add



## ./q/edit
## ./q/del

# Answer

## ./a/add
## ./a/edit
## ./q/repution
## ./a/del
