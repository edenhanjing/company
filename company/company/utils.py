from django.core.paginator import Paginator 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def page_fun(pag_list,paginator):
    p_n = pag_list.number
    page_range = list(range(max(p_n -2,1),p_n))+\
        list(range(p_n,min(p_n + 2, paginator.num_pages)+1))
    if page_range[0] != 1:
        page_range.insert(0,1)
        if p_n - 1 > 3:
            page_range.insert(1,'...')
    if page_range[-1] != paginator.num_pages:
        if paginator.num_pages - p_n >3:
            page_range.insert(paginator.num_pages-2,'...')
        page_range.append(paginator.num_pages)
    return page_range

def activation_html_content(user):
    html_content = '''<div style="margin: auto;width: 500px;border: 1px solid #3c484e;border-radius: 5px;"> 
                <div style="padding: 5px 10px;background: #3c484e;color: #fff;">
                    <span>Hi! {0}.</span>
                </div>
                <div style="padding: 5px 10px;">
                    <p>{1}</p>
                </div></div>'''.format(str(user),'这是一封来自FDD的异步测试邮件！')
    return html_content

def channel_send_msg(room_name,msg):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_name, {"type": "user.message",'message': {'msg':msg}})
    
    

# 装饰器
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
def group_required(*group_names):
   """Requires user membership in at least one of the groups passed in."""
   def in_groups(u):
       if u.is_authenticated:
           if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
               return True
       return False
   return user_passes_test(in_groups)

def anonymous_required(function=None, redirect_url=None):
   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL
   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )
   if function:
       return actual_decorator(function)
   return actual_decorator

import functools
# 访问量
def views_count(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('views_count'):
            views = Views.objects.get_or_create(day=timezone.make_aware(timezone.datetime.today()))[0]
            views.view_num += 1
            views.save()
            request.session['views_count'] = True
            # request.session.set_expiry(200)

        return func(request, *args, **kwargs)
    return wrapper
