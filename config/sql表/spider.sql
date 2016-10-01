--如果有不一样的字段，结合db_operation模块进行修改即可

-- Create table 微博用户表
create table WEIBO_SINA_USERS
(
  SU_ID              VARCHAR2(50) not null,
  SU_SCREEN_NAME     VARCHAR2(100),
  SU_PROVINCE        VARCHAR2(100),
  SU_CITY            VARCHAR2(100),
  SU_DESCRIPTION     CLOB,
  SU_HEADIMG_URL     VARCHAR2(200),
  SU_BLOG_URL        VARCHAR2(200),
  SU_DOMAIN_NAME     VARCHAR2(200),
  SU_GENDER          VARCHAR2(20),
  SU_FOLLOWERS_COUNT NUMBER(11),
  SU_FRIENDS_COUNT   NUMBER(11),
  SU_STATUSES_COUNT  NUMBER(11),
  SU_GENDER_PREFER   VARCHAR2(50),
  SU_BIRTHDAY        VARCHAR2(100),
  SU_BLOOD_TYPE      VARCHAR2(50),
  SU_CONTACT_INFO    CLOB,
  SU_WORK_INFO       CLOB,
  SU_EDUCATE_INFO    CLOB,
  SU_OWNTAG_INFO     CLOB,
  SU_VERIFYTYPE      NUMBER,
  SU_VERIFYINFO      VARCHAR2(500),
  SU_REGISTER_TIME   VARCHAR2(100),
  SU_UPDATE_TIME     VARCHAR2(100)
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 8K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the columns
comment on column WEIBO_SINA_USERS.SU_ID
  is '用户ID,主键';
comment on column WEIBO_SINA_USERS.SU_SCREEN_NAME
  is '用户名';
comment on column WEIBO_SINA_USERS.SU_PROVINCE
  is '省份';
comment on column WEIBO_SINA_USERS.SU_CITY
  is '城市';
comment on column WEIBO_SINA_USERS.SU_DESCRIPTION
  is '简介';
comment on column WEIBO_SINA_USERS.SU_HEADIMG_URL
  is '头像';
comment on column WEIBO_SINA_USERS.SU_BLOG_URL
  is '博客主页';
comment on column WEIBO_SINA_USERS.SU_DOMAIN_NAME
  is '用户的域名';
comment on column WEIBO_SINA_USERS.SU_GENDER
  is '性别';
comment on column WEIBO_SINA_USERS.SU_FOLLOWERS_COUNT
  is '粉丝数';
comment on column WEIBO_SINA_USERS.SU_FRIENDS_COUNT
  is '关注数';
comment on column WEIBO_SINA_USERS.SU_STATUSES_COUNT
  is '微博数';
comment on column WEIBO_SINA_USERS.SU_GENDER_PREFER
  is '性取向';
comment on column WEIBO_SINA_USERS.SU_BIRTHDAY
  is '生日';
comment on column WEIBO_SINA_USERS.SU_BLOOD_TYPE
  is '血型';
comment on column WEIBO_SINA_USERS.SU_CONTACT_INFO
  is '联系方式';
comment on column WEIBO_SINA_USERS.SU_WORK_INFO
  is '工作信息';
comment on column WEIBO_SINA_USERS.SU_EDUCATE_INFO
  is '教育信息';
comment on column WEIBO_SINA_USERS.SU_OWNTAG_INFO
  is '标签';
comment on column WEIBO_SINA_USERS.SU_VERIFYTYPE
  is '认证类型';
comment on column WEIBO_SINA_USERS.SU_VERIFYINFO
  is '认证信息';
comment on column WEIBO_SINA_USERS.SU_REGISTER_TIME
  is '注册时间';
-- Create/Recreate primary, unique and foreign key constraints
alter table WEIBO_SINA_USERS
  add primary key (SU_ID)
  using index
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

-- Create table 微博搜索相关
create table WEIBO_SEARCH_DATA
(
  SE_PRIMARYKEY            VARCHAR2(200) not null,
  SE_MID                   VARCHAR2(50),
  SE_USERID                VARCHAR2(50),
  SE_USERNAME              VARCHAR2(70),
  SE_UHEADIMAGE            VARCHAR2(700),
  SE_SID                   VARCHAR2(40),
  SE_CONTENT               CLOB,
  SE_PICTURE_ADDRESS       CLOB,
  SE_CREATETIME            DATE,
  SE_DEVICE                VARCHAR2(100),
  SE_TOTALREPLYCOUNT       NUMBER(11),
  SE_PRAISE_COUNT          NUMBER(11),
  SE_REPOST_COUNT          NUMBER(11),
  SE_COMMENT_COUNT         NUMBER(11),
  SE_FAVORITE_COUNT        NUMBER(11),
  SE_ISFORWARD             NUMBER(1),
  SE_RETWEET_MID           VARCHAR2(50),
  SE_RETWEET_URL           VARCHAR2(500),
  SE_RETWEET_CONTENT       CLOB,
  SE_RETWEET_PRAISE_COUNT  NUMBER(11),
  SE_RETWEET_REPOST_COUNT  NUMBER(11),
  SE_RETWEET_COMMENT_COUNT NUMBER(11),
  SE_RETWEET_CREATETIME    DATE,
  SE_RETWEET_DEVICE        VARCHAR2(100),
  SE_FETCH_TIME            DATE,
  SE_LOCATION_INFO         VARCHAR2(500),
  SE_SOURCETYPE            VARCHAR2(50),
  SE_KEYWORD               VARCHAR2(300),
  PUBLIC_OPINION_MACHINE   VARCHAR2(100),
  PUBLIC_OPINION_HUMAN     VARCHAR2(100),
  PUBLIC_OPINION_AUDITOR   VARCHAR2(100),
  IS_NEW                   CHAR(1) default 1 not null,
  SENSITIVE_FLAG           NUMBER default 0,
  IS_CRAWLED               NUMBER default 0 not null,
  EMOTION_VALUE            NUMBER default 0 not null
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 3M
    next 8K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the columns
comment on column WEIBO_SEARCH_DATA.SE_PRIMARYKEY
  is '主键';
comment on column WEIBO_SEARCH_DATA.SE_MID
  is '微博id';
comment on column WEIBO_SEARCH_DATA.SE_USERID
  is '用户id';
comment on column WEIBO_SEARCH_DATA.SE_USERNAME
  is '用户名';
comment on column WEIBO_SEARCH_DATA.SE_UHEADIMAGE
  is '用户头像';
comment on column WEIBO_SEARCH_DATA.SE_SID
  is '微博sid';
comment on column WEIBO_SEARCH_DATA.SE_CONTENT
  is '微博内容';
comment on column WEIBO_SEARCH_DATA.SE_PICTURE_ADDRESS
  is '微博图片';
comment on column WEIBO_SEARCH_DATA.SE_CREATETIME
  is '发布时间';
comment on column WEIBO_SEARCH_DATA.SE_DEVICE
  is '发布设备';
comment on column WEIBO_SEARCH_DATA.SE_TOTALREPLYCOUNT
  is '旧项目相关，以前可用api获取，现在通过爬取的方式无法查看，不备注的都是旧项目相关，都不用管了';
comment on column WEIBO_SEARCH_DATA.SE_PRAISE_COUNT
  is '点赞数';
comment on column WEIBO_SEARCH_DATA.SE_REPOST_COUNT
  is '转发数';
comment on column WEIBO_SEARCH_DATA.SE_COMMENT_COUNT
  is '评论数';
comment on column WEIBO_SEARCH_DATA.SE_ISFORWARD
  is '是否是转发';
comment on column WEIBO_SEARCH_DATA.SE_FETCH_TIME
  is '抓取时间';
comment on column WEIBO_SEARCH_DATA.SE_KEYWORD
  is '搜索关键词';
comment on column WEIBO_SEARCH_DATA.IS_NEW
  is '是否是新增数据';
comment on column WEIBO_SEARCH_DATA.SENSITIVE_FLAG
  is '敏感数据计算标记';
comment on column WEIBO_SEARCH_DATA.IS_CRAWLED
  is '是否在后台被爬取过转发关系';
comment on column WEIBO_SEARCH_DATA.EMOTION_VALUE
  is '情感值，用于情感分析';
-- Create/Recreate primary, unique and foreign key constraints
alter table WEIBO_SEARCH_DATA
  add primary key (SE_PRIMARYKEY)
  using index
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );

-- Create table 源微博表
create table WEIBO_SPREAD_ORIGINAL
(
  USER_ID              VARCHAR2(20),
  USER_SCREENNAME      VARCHAR2(64),
  USER_PROVINCE        VARCHAR2(20),
  USER_CITY            VARCHAR2(20),
  USER_LOCATION        VARCHAR2(64),
  USER_DESCRIPTION     VARCHAR2(2048),
  USER_URL             VARCHAR2(128),
  USER_PROFILEIMAGEURL VARCHAR2(128),
  USER_GENDER          VARCHAR2(100),
  USER_FOLLOWERSCOUNT  NUMBER(8),
  USER_FRIENDSCOUNT    NUMBER(8),
  USER_STATUSESCOUNT   NUMBER(8),
  USER_CREATEDAT       VARCHAR2(32),
  USER_VERIFIEDTYPE    NUMBER(8),
  USER_VERIFIEDREASON  VARCHAR2(128),
  STATUS_CREATEDAT     VARCHAR2(32),
  STATUS_MID           VARCHAR2(20),
  STATUS_SOURCE        VARCHAR2(50),
  STATUS_REPOSTSCOUNT  NUMBER(8),
  STATUS_COMMENTSCOUNT NUMBER(8),
  STATUS_URL           VARCHAR2(128)
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 16K
    next 8K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the columns
comment on column WEIBO_SPREAD_ORIGINAL.STATUS_SOURCE
  is '发布设备';
comment on column WEIBO_SPREAD_OTHER.STATUS_URL
  is '当前微博URL';

-- Create table 扩散微博表
create table WEIBO_SPREAD_OTHER
(
  USER_ID              VARCHAR2(20),
  USER_SCREENNAME      VARCHAR2(64),
  USER_PROVINCE        VARCHAR2(20),
  USER_CITY            VARCHAR2(20),
  USER_LOCATION        VARCHAR2(64),
  USER_DESCRIPTION     VARCHAR2(2048),
  USER_URL             VARCHAR2(128),
  USER_PROFILEIMAGEURL VARCHAR2(128),
  USER_GENDER          VARCHAR2(100),
  USER_FOLLOWERSCOUNT  NUMBER(8),
  USER_FRIENDSCOUNT    NUMBER(8),
  USER_STATUSESCOUNT   NUMBER(8),
  USER_CREATEDAT       VARCHAR2(32),
  USER_VERIFIEDTYPE    NUMBER(8),
  USER_VERIFIEDREASON  VARCHAR2(128),
  STATUS_CREATEDAT     VARCHAR2(32),
  STATUS_MID           VARCHAR2(20),
  STATUS_SOURCE        VARCHAR2(50),
  STATUS_REPOSTSCOUNT  NUMBER(8),
  STATUS_COMMENTSCOUNT NUMBER(8),
  UPPER_USER_ID        VARCHAR2(20),
  ORIGINAL_STATUS_ID   VARCHAR2(32),
  STATUS_URL           VARCHAR2(128)
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 16K
    next 8K
    minextents 1
    maxextents unlimited
  );
-- Add comments to the columns
comment on column WEIBO_SPREAD_OTHER.UPPER_USER_ID
  is '上层转发用户ID';
comment on column WEIBO_SPREAD_OTHER.ORIGINAL_STATUS_ID
  is '源微博ID';
comment on column WEIBO_SPREAD_OTHER.STATUS_URL
  is '当前微博URL';
