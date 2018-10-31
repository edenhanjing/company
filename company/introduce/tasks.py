from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail

from django.conf import settings
from django.core.mail import EmailMessage
import company.utils as utils

import company.utils as  utils

#发送邮件
@shared_task
def send_mail_(receiver,msg):
    mail_title='来自FDD的测试邮件'
    mail_content=msg
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = receiver
    send_mail(mail_title,mail_content, from_email,[to_email,],fail_silently=False)

@shared_task
def celery_senm_mail(username,email):
	subject, from_email, to_email = '来自FDD的异步测试邮件', settings.DEFAULT_FROM_EMAIL,email
	html_content = utils.activation_html_content(username)
	msg = EmailMessage(subject, html_content, from_email, [to_email])
	msg.content_subtype = "html"  # Main content is now text/html
	msg.send()

	utils.channel_send_msg('user_'+username,'Celery已发送测试邮件!')
