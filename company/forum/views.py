from django.shortcuts import render
from forum.models import ArticleType,Article,Comment,Collection,LikesNum
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.contenttypes.models import ContentType

from django.core.paginator import Paginator 
from django.db.models import Q

import company.utils as utils 
# Create your views here.
from django.core import serializers
import json



@csrf_exempt
def forum(request):
    context = {}
    articles = Article.objects.all()

    if request.method=='POST':
        print('post')
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        if title and content != '':
            Article(title=title,article_type_id=2,user=request.user,content=content).save()
    
    if request.GET:
        search = request.GET.get('search','')
        if search:
            articles = Article.objects.filter(Q(title__contains=search) | Q(user__username__contains=search))
        articletype_id =request.GET.get('articletype_id',"")
        if articletype_id:
            articles = Article.objects.filter(article_type__id=articletype_id)

    
    ct = ContentType.objects.get_for_model(Article)

    page = request.GET.get('page',1)


    paginator = Paginator(articles,5)
    pag_list = paginator.get_page(page)
    page_range = utils.page_fun(pag_list,paginator)

    context['page_range'] = page_range
    context['articles'] = pag_list
    context['articletypes'] = ArticleType.objects.all()
    context['likesnums'] = LikesNum.objects.filter(content_type=ct).order_by('-likesnum')[:5]
    return render(request,'forum/forum.html',context)

def articletype(request,slug):
    context = {}
    
    context['article'] = Article.objects.filter(article_type__id=slug)
    return render(request,'forum/articletype.html',context)
    
def article(request,slug):
    context = {} 
    article = Article.objects.get(id=slug)
    if request.method == 'POST':
        print(request.POST)
        content = request.POST.get('content','')
        Comment(user=request.user,article_id=slug,content=content).save()
    
    if not request.session.get('article_read_list'):
        request.session['article_read_list'] = []

    if slug not in request.session['article_read_list']:
        article.read_num +=1
        article.save()
        request.session['article_read_list'].append(slug)


    comments = Comment.objects.filter(article_id=slug)
    context['article'] = article
    context['comments'] = comments
    return render(request,'forum/article.html',context) 

@csrf_exempt
def likes(request):
    if request.method == 'POST':
        app_label = request.POST.get('app_label','')
        model = request.POST.get('model','')
        object_id = request.POST.get('object_id','')
        
        response = {}

        
        like_str = app_label+model+object_id
        
        if not request.session.get('like_list',''):
            request.session['like_list'] = []
        if like_str not in request.session['like_list']:
            request.session['like_list'].append(like_str)
            ct = ContentType.objects.get(app_label=app_label, model=model)
            likesnum_query = LikesNum.objects.get_or_create(content_type=ct,object_id=object_id)[0]
            likesnum_query.likesnum += 1
            likesnum_query.save()
            response['likes_ok'] = True
        return JsonResponse(response)

@csrf_exempt
def post_response(request):
    if request.GET.get('article_id',''):
        article_id = request.GET.get('article_id','')
        try:
            article = Article.objects.filter(id=article_id)
            return JsonResponse(json.loads(serializers.serialize('json',article,fields=('title','article_type','user','published','read_num','likesnum'))),safe=False,status=200)
        except:
            return HttpResponse(status=404)

    if request.method=='POST':
        article_id = request.POST.get('article_id','')
        try:
            article = Article.objects.filter(id=article_id)
            return JsonResponse(json.loads(serializers.serialize('json',article,fields=('title','article_type','user','published','read_num','likesnum'))),safe=False,status=200)
        except:
            return HttpResponse(status=404)
    return HttpResponse(status=200)