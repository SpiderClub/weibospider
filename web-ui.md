# 微博爬虫管理ui是使用Django框架完成
## 1.创建管理员账户

首先，我们得创建一个能登录管理页面的用户。请运行下面的命令：

```
python manage.py createsuperuser
```
输入你想使用的用户名，然后回车。

```
Username: admin
```
接着，你会被提示要求输入邮箱：

```
Email address: admin@example.com
```
最后一步是输入密码。你会被要求输入两次密码，第二次的目的是为了确认第一次输入的确实是你想要的密码。

```
Password: ********
Password(again): ********
Superuser created successfully.
```
启动用于开发的服务器

Django 的管理界面默认就是启用的。让我们启动开发服务器，看看它到底是什么样的。

如果服务器还没运行，那就运行下：

```
python manage.py runserver
```
或者运行
```bash
bin/startup.sh
```
现在，打开浏览器，转到你本地域名的 “/admin/” 目录，比如 “http://127.0.0.1:8000/admin” 。你应该会看见管理员登录界面

进入管理页面

现在，试着使用你在上一步中创建的超级用户来登录。然后你将会看到 Django 管理页面的索引页

你将会看到几种可编辑的内容：组和用户。它们由 django.contrib.auth 提供，这是 Django 开发的认证框架。
## 2.建立微博model
#### add model（代码中已存在，可跳过）
```bash
django-admin.py startapp WeiboModel
```
#### make changes
```bash
python manage.py makemigrations WeiboModel
```
#### commit changes to db
```bash
python manage.py migrate WeiboModel
```
## 3.返回界面查看效果

####参考：
如果想要深入理解django，请参考：
https://django-intro-zh.readthedocs.io/zh_CN/latest/part2/#_4

