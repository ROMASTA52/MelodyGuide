from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('news/', views.news, name='news'),
    path('like_dislike/', views.like_dislike, name='like_dislike'),
    path('news/<int:news_item_id>/comment/', views.add_comment, name='add_comment'),
    path('youtube_search/', views.search_youtube, name='youtube_search'),
]
