from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.blog_main), 
    path('register/', views.register),
    path('logout/', views.logout_request),
    path('login/', views.login_request),
    path('searchpost/', views.search_post, name="search"),
    path('profile/', views.profile, name='user_profile'),
    path('profile/<username>', views.look_profile, name='look_profile'),
    path('<slug>/', views.slug_process), #з <> дані передаються в views.blog_main
]
