from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
   # path('', views.index, name='index'),
    path('hello/<int:id>', views.hello),    
    path('', views.login_view, name='login'),  # เส้นทางสำหรับหน้า login
    path('signup/', views.signup_view, name='signup'),  # เส้นทางสำหรับหน้า signup
    path('logout/', views.logout_view, name='logout'),  # เส้นทางสำหรับ logout
    path('course/',views.course,name='course' ),
]