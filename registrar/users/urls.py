from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [  
    path('', views.login_view, name='login'),  # เส้นทางสำหรับหน้า login
    path('signup/', views.signup_view, name='signup'),  # เส้นทางสำหรับหน้า signup
    path('logout/', views.logout_view, name='logout'),  # เส้นทางสำหรับ logout
    path('course/', views.course_list, name='course_list'),
    path('course/request/<int:course_id>/', views.request_quota, name='request_quota'),
    path('quota_success/', views.quota_success, name='quota_success'),
    path('my_quotas/', views.my_quota_requests, name='my_quota_requests'),
    path('cancel_quota/<int:request_id>/', views.cancel_quota_request, name='cancel_quota_request'),

        ] 
 