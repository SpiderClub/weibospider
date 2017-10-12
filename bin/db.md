## 数据库脚本
#### add admin user
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
#### add model
```bash
django-admin.py startapp WeChatModel
```
#### make changes
```bash
python manage.py makemigrations WeChatModel
```
#### commit changes to db
```bash
python manage.py migrate WeChatModel
```

