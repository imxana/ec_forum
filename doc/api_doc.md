# Error

ErrorType|code|codeState
------------ | ------------- | ------------
normalError          | -10 | something bad happended 
safeError            | -11 | unsafe attempt, who R U 
requestError         | -12 | method not allowed      
serverError          | -13 | server error            
methodAbort          | -14 | method already aborted  
- | - | -
userNotExisted       | -20 | user not existed        
usernameEmpty        | -21 | username empty          
usernameExisted      | -22 | username exists         
usernameIllegal      | -23 | username illegal        
useridEmpty          | -24 | userid empty            
watchuserNotExisted  | -25 | watch user not existed  
userAlreadyWatched   | -26 | user already watched    
userAlreadyUnwatched | -27 | user already unwatched  
- | - | -
pswEmpty             | -30 | password empty          
pswWrong             | -31 | wrong password          
pswIllegal           | -32 | psw illegal             
- | - | -
emailNotExisted      | -40 | email not existed       
emailEmpty           | -41 | email empty             
emailExisted         | -42 | email is existed        
emailIllegal         | -43 | email illegal           
emailNotConfirmed    | -44 | email not confirmed     
emailConfirmed       | -45 | email confirmed already 
emailNotChanged      | -46 | email not changed       
- | - | -
loginNameNotExisted  | -50 | login name not existed  
loginNameEmpty       | -51 | login name empty        
loginNameIllegal     | -52 | login name illegal      
- | - | -
articleTitleEmpty    | -60 | article title empty     
articleTitleIllegal  | -61 | article title illegal   
articleTextEmpty     | -62 | article text empty      
articleNotExisted    | -63 | article not existed     
articleidEmpty       | -64 | article id empty        
articleAccess        | -65 | no access to modify article
articleExist         | -66 | article exists          
articleStarAlready   | -67 | article star already    
articleNotStar       | -68 | article not star        
articleRecommended   | -69 | article recommend already
articleNotRecommend  | -6A | article not recommend   
articleSelfAction    | -6B | article self action     
- | - | -
verifyEmpty          | -70 | verify code empty       
verifyWrong          | -71 | verify code wrong       
argsIllegal          | -72 | illegal arguments value 
argsEmpty            | -73 | empty arguments value   
tagNotExisted        | -74 | some tag not existed    
tagNotIllegal        | -75 | tags not illegal        
- | - | -
commentTextEmpty     | -80 | comment text empty      
commentEventNotExsited|-81 | comment event not exists
commentidEmpty       | -82 | comment id empty        
commentNotExisted    | -83 | comment not existed     
commentExsited       | -84 | comment exists in event 
commentAccess        | -85 | no access to modify comment
commentLikeAlready   | -86 | comment like already    
commentDislikeAlready| -87 | comment dislike already 
commentSelfAction    | -88 | comment self action     
- | - | -
questionTitleEmpty   | -90 | question title empty    
questionTitleIllegal | -91 | question title illegal  
questionTextEmpty    | -92 | question text empty     
questionNotExisted   | -93 | question not existed    
questionidEmpty      | -94 | question id empty       
questionAccess       | -95 | no access to modify question
questionExist        | -96 | question exists         
questionStarAlready  | -97 | question star already   
questionNotStar      | -98 | question not star       
questionLikeAlready  | -99 | question like already   
questionDislikeAlready|-9B | question dislike already
questionSelfAction   | -9D | question self action    
- | - | -
answerTextEmpty      | -A0 | answer text empty       
answerNotExisted     | -A1 | answer not existed      
answeridEmpty        | -A2 | answer id empty         
answerAccess         | -A3 | no access to modify answer
answerExist          | -A4 | answer exists           
answerStarAlready    | -A5 | answer star already     
answerNotStar        | -A6 | answer not star         
answerLikeAlready    | -A7 | answer like already     
answerDislikeAlready | -A8 | answer dislike already  
answerSelfAction     | -A9 | answer self action      
- | - | -
reputationNotEnough  | -B0 | reputation not enough [ now_repu: 0, request_repu: 99999 ]

# Public

## 获取所有基础tag ./public/tags

method:get

return: array

## 获取5位随机验证码 ./public/get_verify

method:get

return: str

## 获取密钥 ./safe/secret_key (上线之后文档将不显示此API)

method:get

return: str

## 全局搜索 ./search

method:get

字段|类型|要求
------------ | ------------- | ------------
word | str | 

return

字段|类型|备注
------------ | ------------- | ------------
code | 1 |-
u_ids|str|按照名字搜索
t_ids|str|按照标题搜索
q_ids|str|按照标题搜索
a_ids|str|按照回答内容搜索




# 账户接口 Acount 

## 注册 ./sign_up

method:post

字段|类型|要求
------------ | ------------- | ------------
u_email|str|[ A-Za-z0-9\_\.]+@[A-Za-z0-9\.]+\.[A-Za-z]{2,4}
u_name|str| [a-z][a-z0-9\.]{2,20}
u_psw|str|[6,16]


suc:

字段|类型或值
------------ | -------------
code|1
u_id|int


fail:

字段|类型或值
------------ | -------------
code| 21/30/41 23/32/43 22/42 12/13
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
code| 51/30 52 40/50 31 12/13
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
code | 12/13/14 24/30 20 31
codeState | str


# User_info

## 查询用户信息 ./u/query

method:get

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填

suc:

字段|类型或值
------------ | -------------
code|1
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
code| 12/13 24 20
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
code| 12/13 24/30 20 31
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
code| 12/13 24/72/73 31 26/27
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

fail:

字段|类型或值
------------ | -------------
code| 12 24/41/70 20 43
codeState| str


## 邮箱验证通过 ./u/email/confirm

『这个方法将直接后台修改验证状态为 「已验证」，所以需要前台验证码判断，以最新收到的验证码为准』

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
code| 12/13 24/30 20 31
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
code| 12/13 24/30/41 20 31 46
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
code| 12/13 24/30 20 32/31
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
code| 12/13 51/52 20/40
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
code| 12/13 24/30 20 32
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
history | ^(history array)

^history info

字段|类型或值
------------ | -------------
rep | int
action | str
date | int



fail:

字段|类型或值
------------ | -------------
code| 12/13 24/30 20 31
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
code| 12/13 24/30/60/62 75 20 31
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
code | 12/13 24/30/64 20/63 31 
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
code | 12/13 24/30/64 20/63 31 65
codeState | str


## 获取展示文章列表 ./t/display


method:get

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
code | 12/13 75
codeState | str

## 查询文章信息 ./t/query

method:get

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
t_like | int
t_comments | str
t_tags | str
t_date_latest | int
t_star | int

fail:

字段|类型或值
------------ | -------------
code | 12/13 63/64
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
code | 12/13 24/30/64/73/72 20/63 31 67/68
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
code | 12/13 24/30/64 20/66 31
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
code | 12/13 24/30/64/73/72 20/63 31 69/6A
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
code| 12/13 24/30/80/73 72 20/81 31
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
code | 12/13 24/30/82 20/83 31 85
codeState | str

## 查询评论信息 ./c/query

method:get

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
c_like | int


fail:

字段|类型或值
------------ | -------------
code | 12/13 82 83
codeState | str

## 评论点赞 ./c/like

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
c_id | int
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
code | 12/13 24/30/82/73/72 20/83 31 86/87/88
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
code| 12/13 24/30/90/92 75/20 31
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
code | 12/13 24/30/90/92/94 20/93 31
codeState | str

## 删除问题 ./q/del

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
code | 12/13 24/30/94 20/93 31 95
codeState | str


## 获取问题展示列表 ./q/display


method:get

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
code | 12/13 75
codeState | str

## 查询问题信息 ./q/query

method:get

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
q_like | int
q_close | int
q_report | int
q_answers | str
q_comments | str
q_date_latest | int
q_star | int

fail:

字段|类型或值
------------ | -------------
code | 12/13 94 93
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
code | 12/13 24/30/94 20/93 31
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
code | 12/13 24/30/94/73/72 20/93 31 97/98
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
code | 12/13 24/30/94 20/96 31
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
code | 12/13 24/30/94/73/72 20/93 31 99/9B/9D
codeState | str



# Answer



## 添加回答 ./a/add

method:post

字段|类型|要求
------------ | ------------- | ------------
u_id | int | 必填
u_psw | str | 用于验证
q_id | int | 必填
a_text | str | 非空


suc:

字段|类型或值
------------ | -------------
code | 1
a_id | int


fail:

字段|类型或值
------------ | -------------
code| 12/13 24/30/94/A0 20/93 31 
codeState| str


## 更新问题信息./a/update

method:post

字段|类型
------------ | -------------
u_id | int
u_psw | str
a_id | int
a_text| str

suc:

字段|类型或值
------------ | -------------
code|1

fail:

字段|类型或值
------------ | -------------
code | 12/13 24/30/A0 20/A1 31 B0
codeState | str

## 删除答案 ./a/del

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
a_id | int


suc:

字段|类型或值
------------ | -------------
code|1
a_id | int

fail:

字段|类型或值
------------ | -------------
code | 12/13 24/30/A0 20/A1 31 A3
codeState | str





## 查询回答信息 ./a/query

method:get

字段|类型
------------ | -------------
a_id | int

suc:

字段|类型或值
------------ | -------------
code | 1
a_id | int
u_id | int
a_text | str
a_date | int
a_like | int
a_comments | str
a_star | int
a_date_latest | int

fail:

字段|类型或值
------------ | -------------
code | 12/13 A2 A1
codeState | str


## 查询回答信息UI ./a/query_pro

method:post

字段|类型
------------ | -------------
a_id | int
u_id | int
u_psw | str

suc:

字段|类型或值
------------ | -------------
code | 1
a_star_bool | 1/0
a_like_state | 1/0/-1

fail:

字段|类型或值
------------ | -------------
code | 12/13 24/30/A2 20/A1 31
codeState | str

## 收藏回答 ./a/star


method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
a_id | int
u_act | str(1表示收藏,0表示取消收藏)

suc:

字段|类型或值
------------ | -------------
code | 1
r_id | int(如果u_act=='0'则无此参数)

fail:

字段|类型或值
------------ | -------------
code | 12/13 24/30/A2/73 20/A1 31 A5/A6
codeState | str

## 静默移除失效收藏回答 ./a/star_unlink

method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
a_id | int

suc:

字段|类型或值
------------ | -------------
code | 1

fail:

字段|类型或值
------------ | -------------
code | 12/13 24/30/A2 20/A4 31
codeState | str

## 赞同回答 ./a/like


method:post

字段|类型
------------ | -------------
u_id | int
u_psw| str
a_id | int
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
code | 12/13 24/30/A2/73 20/A1 31 A7/A8/A9
codeState | str


# Image

## 上传图片 

使用对应七牛sdk，[下载地址](http://developer.qiniu.com/resource/official.html#sdk)

参数|类型或值
------------ | -------------
'access_key' | 'iQ3ndG5uRpwdeln_gcrH3iiZ7E3KbMdJVkdYV9Im',
'secret_key' | 'AGsp6K7fu1NsH2DnsPi7hW3qa3JXb4dtfeGvkm-A',
'bucket_name' | 'image',
'bucket_domain' | 'https|//oi3qt7c8d.qnssl.com/',
'callbakUrl' | 'http|//139.129.24.151/image/upload',
'callbackBody' | 'filename:$(fname)&secret_key:$(secret_key)'

## 下载图片

get

bucket_domain + filename





