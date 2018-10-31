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