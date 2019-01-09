# django-demo
Django的基础，流行功能展示。这是一个囊括众多django功能的演示项目。
包含基础的admin,auth,contenttypes,sessions,messages运用。
扩展celery实现异步任务、定时任务，扩展channels（websocket）实现实时前后台交互。

# 使用
1.建议ubuntu上运行。安装python3.6+，Django2+，MySql，扩展需简单安装RabbitMQ，Redis。
2.新建一个env，安装项目所需库 pip install -r requirements.txt。
3.mysql新建一个指定utf8的数据库company，CREATE DATABASE company CHARACTER SET utf8。
5.修改company/settings.py中的邮箱配置、数据库配置
6.django创建数据表，python manage.py makemigrations。
7.试验启动项目，python manage.py runserver。

# 展示
http://18.220.137.15

# 部署提示
采用Nginx（反向代理、静态文件代理），daphne（应用服务），supervisor（守护进程）
