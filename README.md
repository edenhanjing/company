# django-demo
Django的基础，流行功能展示。这是一个囊括众多django功能的演示项目。
包含基础的admin,auth,contenttypes,sessions,messages运用。
扩展celery实现异步任务、定时任务，扩展channels（websocket）实现实时前后台交互。

# 使用
1.建议ubuntu上运行。安装python3.6+，Django2+，MySql，（扩展需简单安装并配置RabbitMQ，Redis）。 <br> 
2.新建一个env，安装项目所需库 pip install -r requirements.txt。<br> 
3.django创建数据表，python manage.py makemigrations ，python manage.py migrate。 <br> 
4.试验启动项目，python manage.py runserver。 

# 部署提示
采用Nginx（反向代理、静态文件代理），daphne（应用服务），supervisor（守护进程）

