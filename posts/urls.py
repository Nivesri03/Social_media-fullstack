from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.create_post, name='create'),
    path('<int:post_id>/', views.post_detail, name='detail'),
    path('<int:post_id>/edit/', views.edit_post, name='edit'),
    path('like/', views.like_post, name='like'),
    path('save/', views.save_post, name='save'),
    path('share/', views.share_post, name='share'),
    path('delete/', views.delete_post, name='delete'),
    path('comment/add/', views.add_comment, name='add_comment'),
    path('comment/like/', views.like_comment, name='like_comment'),
    path('search/', views.search_posts, name='search'),
]
