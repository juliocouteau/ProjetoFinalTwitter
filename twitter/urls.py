from django.urls import path
from . import views  # IMPORTANTE: Apenas um ponto "."
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_users, name='search_users'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),
    path('retweet/<int:post_id>/', views.retweet, name='retweet'),
    path('notifications/', views.notifications, name='notifications'),
]