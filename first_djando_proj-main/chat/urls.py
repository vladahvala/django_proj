from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.load_messages_home),
    path('search_user/', views.search_user, name="search_user")    
]