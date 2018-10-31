from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
# Create your views here.
from django.utils.safestring import mark_safe
import json



def chat(request):
	context = {}

	return render(request,'chat/chat.html',context)

    
@login_required
def chat_room(request,room_name):
    return render(request, 'chat/chat_room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })