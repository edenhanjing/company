
from django.shortcuts import render,redirect
from .models import CompanyInfo,Department
#from introduce.models import CompanyInfo,Department
from django.http import JsonResponse,HttpResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required 


from django.conf import settings
import introduce.tasks as celery_task
import company.utils as  utils
import os
# Create your views here.
def index(request):
	context = {}
	#print(request)
	context['companyinfo'] = CompanyInfo.objects.get(id=1)
	context['department'] = Department.objects.filter(company_id=1)

	
	return render(request,'introduce/index.html',context)

def department(request):
	context = {}
	return render(request,'introduce/department.html',context)


def celery_send_maile(request):
	if not  request.user.is_authenticated:
		return JsonResponse({'status':"error-User not logged in"})
	
	if 'hassendmail' in request.session:
		return JsonResponse({'status':"error-Already sent once!"})

	utils.channel_send_msg('user_'+request.user.username,'后台已收到发送邮件任务!')
	#发送验证邮件---------------------------
	if request.user.email:
		celery_task.celery_senm_mail.delay(request.user.username,request.user.email)
		request.session['hassendmail'] = True
		return JsonResponse({'status':"success"})
	else:
		return JsonResponse({'status':"error-The current user has not set a mailbox!"})

@login_required
def download_avater(request):
    avatar_url = os.path.join('media',str(request.user.avatar))
    #file_name = os.path.basename(str(request.user.avatar))
    response = FileResponse(open(avatar_url, 'rb'))
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename="user_avater.jpg"'
    utils.channel_send_msg('user_'+request.user.username,'所需下载的文件已准备好。')
    return response 
