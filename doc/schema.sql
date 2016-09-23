create database ec_forum;

use ec_forum;


create table ec_user
(
    u_id integer primary key,
    u_name text,
    u_psw text,
    u_email text,
    u_email_confirm integer,
    u_level integer,
    u_reputation integer,
    u_realname text,
    u_blog text,
    u_github text,
    u_articles text,
    u_questions text,
    u_answers text,
);

create table ec_question
(
    q_id integer,
    u_id integer,
    q_title text,
    q_text text,
    q_date date
);

create table ec_answer
(
    a_id integer primary key,
    u_id integer,
    a_text text,
    a_date date,
    a_reputation integer

);

create table ec_article
(
    t_id integer primary key,
    u_id integer,
    t_title text,
    t_text text,
    t_date date,
    t_reputation integer

);

create table ec_comment
(
    c_id integer primary key,
    t_id integer,
    u_id integer,
    c_text text,
    a_date date
);

create table ec_reputaion
(
    r_id integer,
    type text,
    id integer,
    ua_id integer,
    ub_id integer
);

