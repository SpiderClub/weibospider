create table weibo.keywords
(
	id int not null auto_increment
		primary key,
	keyword varchar(200) not null comment '搜索关键词',
	enable int default '1' null comment '搜索关键词是否需要使用',
	constraint keywords_id_uindex
		unique (id),
	constraint keywords_keyword_uindex
		unique (keyword)
)
comment '搜索关键词表'
;



create table weibo.keywords_wbdata
(
	id int not null auto_increment
		primary key,
	keyword_id int null comment '关键词主键id',
	wb_id varchar(200) null comment '微博id，注意不是微博数据表主键id',
	constraint keywords_wbcont_id_uindex
		unique (id)
)
;

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
	home_crawled int default '0' null,
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

create table weibo.weibo_comment
(
	id int not null auto_increment comment '主键id'
		primary key,
	comment_id varchar(50) null comment '评论id',
	comment_cont varchar(5000) default '' null comment '评论内容',
	weibo_id varchar(200) null comment '微博id',
	user_id varchar(20) null comment '用户id',
	create_time varchar(200) null,
	constraint weibo_comment_id_uindex
		unique (id),
	constraint weibo_comment_comment_id_uindex
		unique (comment_id)
)
comment '微博评论表'
;

create table weibo.weibo_data
(
	id int not null auto_increment comment '主键id'
		primary key,
	weibo_id varchar(200) not null comment '微博id',
	weibo_cont varchar(6000) null,
	repost_num int default '0' null comment '转发数',
	comment_num int default '0' null comment '评论数',
	praise_num int default '0' null comment '点赞数',
	uid varchar(20) not null comment '该微博用户id',
	is_origin int default '1' null comment '是否是源微博，1 是源微博，0 是转发微博',
	device varchar(200) default '' null comment '微博发布设备',
	weibo_url varchar(300) not null comment '微博url',
	create_time varchar(200) null comment '微博创建时间',
	comment_crawled int default '0' null,
	repost_crawled int default '0' null,
	constraint weibo_data_id_uindex
		unique (id),
	constraint weibo_data_weibo_id_uindex
		unique (weibo_id)
)
comment '微博数据表'
;

create index weibo_data_weibo_id_index
	on weibo_data (weibo_id)
;

create table weibo.weibo_repost
(
	id int not null auto_increment
		primary key,
	user_id varchar(20) null comment '微博用户id',
	weibo_id varchar(200) null comment '微博id',
	parent_user_id varchar(20) null comment '上层用户id',
	repost_time varchar(200) null comment '转发时间',
	repost_cont varchar(5000) default '' null comment '转发内容',
	weibo_url varchar(200) null comment '转发微博url',
	parent_user_name varchar(200) null,
	user_name varchar(200) null,
	root_weibo_id varchar(200) null,
	constraint repost_id_uindex
		unique (id),
	constraint weibo_repost_weibo_id_uindex
		unique (weibo_id)
)
;


INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('2891529877', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('2709820275', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1195908387', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1604363024', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('10503', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1819309485', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1853923717', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1565668374', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1751401422', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1758453771', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('2041028560', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1191258123', 0, 0);
INSERT INTO weibo.seed_ids (uid, is_crawled, other_crawled) VALUES ('1839256234', 0, 0);

INSERT INTO weibo.keywords (keyword, enable) VALUES ('择天记', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('胡歌客串', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('奶茶妹', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('火影', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('跑男', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('马云', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('腾讯', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('互联网安全', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('锤子手机', 1);
INSERT INTO weibo.keywords (keyword, enable) VALUES ('外星人', 1);