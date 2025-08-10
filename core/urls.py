from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('reels/', views.reels, name='reels'),
    path('explore/', views.explore, name='explore'),
    path('notifications/', views.notifications, name='notifications'),
    path('messages/', views.messages, name='messages'),
    path('api/notification-count/', views.notification_count, name='notification_count'),
    path('api/message-count/', views.message_count, name='message_count'),
    path('api/send-message/', views.send_message, name='send_message'),
]
