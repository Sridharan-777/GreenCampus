from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('<int:pk>/rsvp/', views.event_rsvp_toggle, name='event_rsvp'),
    path('<int:pk>/attend/<int:user_id>/', views.event_confirm_attendance, name='event_attend'),
]
