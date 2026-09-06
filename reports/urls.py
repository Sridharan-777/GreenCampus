from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('submit/', views.report_create, name='report_create'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('<int:pk>/verify/', views.report_verify, name='report_verify'),
]
