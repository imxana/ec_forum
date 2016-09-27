# Acount
## 注册 ./sign_up

method:post

字段|类型|要求
------------ | ------------- | ------------
u_name| str|str
u_email| str|前台正则验证合法
u_psw| str|前台验证合法



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


fail:

字段|类型或值
------------ | -------------
code|!1
codeState| str


## 删除用户（仅测试用） ./sign_del

method:post

字段|类型
------------ | -------------
u_name/u_email| str
u_psw| str
salt| str


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

## ./u/query

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | str | 必填

suc:

字段|类型或值
------------ | -------------
code|1
u_id|int
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



fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## ./u/update

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | str | 必填
u_psw | str | 用于验证
u_realname | str | 无要求
u_blog | str | 无要求
u_github | str | 无要求
u_watchusers | str | 无要求
u_tags | str | 无要求

suc:

字段|类型或值
------------ | -------------
code|1


fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str


## ./u/email/confirm

## ./u/email/change



## ./u/psw_change



# Article

## ./t/add

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | str | 必填
u_psw | str | 用于验证
u_title | str | 非空
u_text | str | 非空
u_tags | str | 无要求


suc:

字段|类型或值
------------ | -------------
code | 1
t_id | str


fail:

字段|类型或值
------------ | -------------
code|<=0
codeState| str

## ./t/update
## ./t/del
## ./t/show
## ./t/display
## ./t/query
## ./q/repution

# Comment

## ./c/add
## ./c/del

# Question

## ./q/add
## ./q/edit
## ./q/del

# Answer

## ./a/add
## ./a/edit
## ./q/repution
## ./a/del
