from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('rewards/', views.rewards_store, name='rewards_store'),
    path('rewards/redeem/<int:pk>/', views.redeem_reward, name='redeem_reward'),
    path('api/chart-data/', views.chart_data_api, name='chart_data_api'),
]
