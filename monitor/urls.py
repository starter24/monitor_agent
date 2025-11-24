from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.start_monitor),
    path('stop/', views.stop_monitor),
    path('status/', views.get_status),
]
