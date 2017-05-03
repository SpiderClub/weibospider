create table weibo.login_info
(
	id int not null auto_increment
		primary key,
	name varchar(100) null,
	password varchar(200) not null,
	enable int default '1' not null,
	constraint login_info_id_uindex
		unique (id),
	constraint login_info_name_uindex
		unique (name)
)
comment '微博登录账号数据表'
;

create table weibo.seed_ids
(
	id int not null auto_increment
		primary key,
	uid varchar(20) not null comment '微博的用户id',
	is_crawled int default '0' not null comment '该id是否被爬取过,0表示未爬取，1表示已经爬取，2表示爬取出错',
	other_crawled int default '0' not null comment '是否抓取了该用户的前五页粉丝和关注用户的ID，1为已经抓取，0为未抓取，默认是0',
	constraint seed_ids_uid_uindex
		unique (uid)
)
;

create index seed_ids_uid_index
	on seed_ids (uid)
;

create table weibo.wbuser
(
	id int not null auto_increment
		primary key,
	uid varchar(20) null comment '用户id',
	name varchar(200) not null comment '用户昵称',
	gender int default '0' null comment '0表示未知，1表示男，2表示女',
	birthday varchar(200) null,
	location varchar(100) null,
	description varchar(500) null,
	register_time varchar(200) null,
	verify_type int default '0' null comment '1表示个人认证，2表示企业认证,0表示未认证',
	follows_num int default '0' null comment '关注数',
	fans_num int default '0' null comment '粉丝数',
	wb_num int default '0' null comment '微博数',
	level int default '0' null comment '微博等级',
	tags varchar(500) null comment '微博标签',
	contact_info varchar(300) null comment '联系信息',
	education_info varchar(300) null comment '教育信息',
	head_img varchar(500) null comment '用户头像URL',
	work_info varchar(500) null,
	verify_info varchar(300) null,
	constraint wbuser_id_uindex
		unique (id),
	constraint wbuser_uid_uindex
		unique (uid)
)
comment '微博用户表'
;

