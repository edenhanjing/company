from django.urls import path
from . import views

app_name = 'newuser'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('userview/',views.userview,name='userview'),
    path('modify_info/',views.modify_info,name='modify_info'),

    
]