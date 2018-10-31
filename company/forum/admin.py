from django.contrib import admin

# Register your models here.
from forum.models import ArticleType,Article,Comment,Collection,LikesNum
from django import forms 
from django.db import models

class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'type_introduce')
    formfield_overrides = {
        models.TextField:{
            'widget':forms.Textarea(
                attrs={
                'rows':20,
                }
                )
        }
    }

class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField:{
            'widget':forms.Textarea(
                attrs={
                'rows':20,
                }
                )
        }
    }
    list_display = ('title','user','created_time', 'read_num','likes')
    list_filter  =  [ 'created_time' ]
    search_fields  = ['title']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id','user','article_id','created_time', 'content','likes')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')

class LikesNumAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'likesnum')

admin.site.register(ArticleType, ArticleTypeAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(LikesNum, LikesNumAdmin)

