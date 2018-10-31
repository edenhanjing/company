from django.urls import path
from . import views

app_name = 'others'
urlpatterns = [
    #path('',views.forum,name='forum'),
    path('problems_36/',views.problems_36,name='problems_36'),
    path('tiangou/',views.tiangou,name='tiangou'),
]