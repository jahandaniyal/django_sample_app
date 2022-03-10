# -*- coding: utf-8 -*-

from django.urls import path, re_path

from app import views

urlpatterns = [
    path('user/', views.UsersAPIView.as_view(), name='users'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('usage_types/', views.UsageTypesAPIView.as_view(), name='usage_types'),
    re_path(r'usage_type/(?P<usage_type_id>[^/]+)$', views.UsageTypeAPIView.as_view(), name='usage_type'),
    re_path(r'user/(?P<user_id>[^/]+)$', views.UserAPIView.as_view(), name='user'),
    re_path(r'user/(?P<user_id>[^/]+)/usage/(?P<usage_id>[^/]+)/$', views.UsageAPIView.as_view(), name='usage'),
    re_path(r'user/(?P<user_id>[^/]+)/usage$', views.UsagesAPIView.as_view(), name='usages'),
]
