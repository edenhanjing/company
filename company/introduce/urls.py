from django.urls import path
from . import views

app_name = 'introduce'
urlpatterns = [
    path('',views.index,name='index'),
    path('department/',views.department,name='department'),
    #path('pay_test/',views.pay_test,name='pay_test'),
    path('celery_send_maile/',views.celery_send_maile,name='celery_send_maile'),
    path('download_avater/',views.download_avater,name='download_avater'),

]


