from django.shortcuts import render
from django.contrib import auth,messages
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required 
from forum.models import Article
from newuser.models import NewUser
from django.core.paginator import Paginator 
import company.utils as utils 
from django.views.decorators.csrf import csrf_exempt
import re,os
# Create your views here.

def register(request):
    context = {}
    errors = []
    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('用户名不能为空')
        else:
            username = request.POST.get('username')
            if len(username)>4 and re.search(r'^[A-Za-z0-9_]+$', username): 
                try:
                    NewUser.objects.get(username=username)
                
                    errors.append('用户名存在,请修改后注册.') 
                except : 

                    username = request.POST.get('username')
            else:
                errors.append('用户名有问题，不能注册。字符太少或含用奇怪字符!') 

        if not request.POST.get('password'):
            errors.append('密码不能为空')
        else:
            password = request.POST.get('password')


        if not request.POST.get('password2'):
            errors.append('确认密码不能为空')
        else:
            password2 = request.POST.get('password2')
            if password != password2:
                errors.append('两次输入密码不一致')


        if not errors:   
            user = NewUser.objects.create_user(username=username,password=password,nickname=username)
            user.save()

            userlogin = auth.authenticate(username=username,password = password)
            auth.login(request,userlogin)
        

            return HttpResponseRedirect('/newuser/modify_info/')
    context['errors'] = errors

    return render(request,'newuser/register.html',context)

def login(request):
    context = {}
    errors =[]
    username = None
    password = None
    if request.method == "POST":
        if not request.POST.get('username'):
            errors.append('用户名不能为空')
        else:
            username = request.POST.get('username')

        if not request.POST.get('password'):
            errors = request.POST.get('密码不能为空')
        else:
            password = request.POST.get('password')

        if username is not None and password is not None:
            user = auth.authenticate(request,username=username,password=password)
            if user :
                if user.is_active:
                    auth.login(request,user)
                    return HttpResponseRedirect('/')
                else:
                    errors.append('未激活用户')
            else:
                errors.append('用户名或密码错误')

    
    messages.warning(request, errors)
    return render(request,'newuser/login.html',context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def userview(request):
    context = {}
    articles = Article.objects.filter(user=request.user)

    paginator = Paginator(articles,10)
    article_list = paginator.get_page(request.GET.get('page',1))
    page_range = utils.page_fun(article_list,paginator)

    context['page_range'] = page_range
    context['article_list'] = article_list
    return render(request,'newuser/userview.html',context)

@csrf_exempt
@login_required
def modify_info(request):
    context = {}
    if request.method=='POST':
        user = NewUser.objects.get(id=request.user.id)
        if request.FILES:
            user.avatar.delete()
            user.avatar = request.FILES.get('avatar')
            user.save()
            return JsonResponse({"status":"success"})
        else:
            user.nickname = request.POST.get("nickname",'')
            user.profile = request.POST.get("profile",'')
            user.email = request.POST.get("email",'')
            user.save()


    return render(request,'newuser/modify_info.html',context)

