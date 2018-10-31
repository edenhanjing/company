from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('',views.forum,name='forum'),
    path('articletype/<int:slug>',views.articletype,name='articletype'),
    path('article/<int:slug>',views.article,name='article'),
    path('likes/',views.likes,name='likes'),

    path('post_response/',views.post_response,name='post_response'),
    
]