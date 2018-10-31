from django.contrib import admin
import xadmin
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

class ArticleAdmin_(object):
    # 列表显示
    list_display = ['title','article_type','user','created_time', 'read_num','likes']
    # 搜索范围
    search_fields = ['title','user',]
    # 列表过滤
    list_filter = ['title','user',]
    # 默认排序,'-':倒序,从大到小
    ordering = ['-created_time']
    # 只读
    #readonly_fields = ['star']
    # 刷新秒数
    refresh_times = [3,5]
    # 直接编辑
    list_editable = ['title','article_type','likes']
xadmin.site.register(Article,ArticleAdmin_)

class CommentAdmin_(object):
    # 列表显示
    list_display = ['user','article','created_time', 'content','likes']
    # 搜索范围
    search_fields = ['user','article']
    # 列表过滤
    list_filter = ['user']
    # 默认排序,'-':倒序,从大到小
    ordering = ['-created_time']
    # 只读
    #readonly_fields = ['star']
    # 刷新秒数
    refresh_times = [3,5]
    # 直接编辑
    list_editable = ['content','likes']
    def queryset(self):
        '''
        过滤，将被封杀的作者过滤掉
        :return:
        '''
        qs = super(CommentAdmin_, self).queryset()
        #qs = qs.filter(likes__gte=0)
        return qs

xadmin.site.register(Comment,CommentAdmin_)