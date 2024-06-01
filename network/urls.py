
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.loginFunc, name="login"),
    path("logout", views.logoutFunc, name="logout"),
    path("following", views.following, name="following"),
    path("user/<int:user_id>", views.user, name="user"),
    path("register", views.registerFunc, name="register"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    path("like/<int:post_id>", views.like, name="like"),
    path("post/<int:post_id>", views.post, name="post"),
    path('search', views.search, name='search'), 
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
]
