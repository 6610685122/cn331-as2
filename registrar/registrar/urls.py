"""
URL configuration for registrar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('users.urls','users'), namespace='users')),
    path('course/', views.course_list, name='course_list'),
    path('course/request/<int:course_id>/', views.request_quota, name='request_quota'),
    path('quota_success/', views.quota_success, name='quota_success'),
    path('book/', include(('book.urls','book'), namespace='book')),
    path('my_quotas/', views.my_quota_requests, name='my_quota_requests'),
    path('cancel_quota/<int:request_id>/', views.cancel_quota_request, name='cancel_quota_request'),
    path('course/request/<int:course_id>/', views.request_quota, name='request_quota'),
    path('quota_success/', views.quota_success, name='quota_success'),
    path('my_quotas/', views.my_quota_requests, name='my_quota_requests'),
    path('cancel_quota/<int:request_id>/', views.cancel_quota_request, name='cancel_quota_request'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
