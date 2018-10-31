from django.db import models
from newuser.models import NewUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class LikesNum(models.Model):
    likesnum = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.likesnum)
    class Meta:
        verbose_name = '点赞统计'
        verbose_name_plural = verbose_name

class ArticleType(models.Model):
    type_name = models.CharField(max_length=256) 
    type_introduce = models.TextField(default="")
    
    def __str__(self):
        return self.type_name
    class Meta:
        verbose_name = '文章类型'
        verbose_name_plural = verbose_name
    
class Article(models.Model):
    title = models.CharField(max_length=256,verbose_name='标题')
    article_type = models.ForeignKey(ArticleType,on_delete=models.CASCADE,verbose_name='类型')
    user = models.ForeignKey(NewUser,on_delete=models.CASCADE,verbose_name='作者')
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_date = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    published = models.BooleanField(default=0)
    read_num = models.IntegerField(default=0,verbose_name='阅读数')
    likesnum = GenericRelation(LikesNum,related_query_name='article_likes',verbose_name='点赞数')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time'] 
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def likes(self):
        article = Article.objects.get(id=self.id)
        try:
            likesnum = article.likesnum.get(object_id=self.id).likesnum
        except:
            likesnum = 0
        return likesnum
        '''
        ct = ContentType.objects.get_for_model(self)
        ln = LikesNum.objects.get(content_type__pk=ct.id, object_id=self.id)
        return ln.likesnum
        '''

class Comment(models.Model):
    user = models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,null=True,on_delete=models.CASCADE)
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=True)
    likesnum = GenericRelation(LikesNum,related_query_name='comment_likes')

    def __str__(self):
        return self.content
    class Meta:
        ordering = ['-created_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def likes(self):
        comment = Comment.objects.get(id=self.id)
        try:
            likesnum = comment.likesnum.get(object_id=self.id).likesnum
        except:
            likesnum = 0
        return likesnum


class Collection(models.Model):
    user = models.ForeignKey(NewUser,null=True,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,null=True,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.title
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name


