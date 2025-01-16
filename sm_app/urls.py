"""Defines URL patterns for sm_app"""

from django.urls import path

from . import views

app_name = 'sm_app'
urlpatterns = [
    # Home page
    path("", views.index, name='index'),
    # Page for adding new posts
    path('new_post/', views.new_post, name='new_post'),
    # Page for editing existing posts
    path('edit_post/<int:entry_id>', views.edit_post, name='edit_post'),

    path('profiles/', views.profiles, name='profiles'),
    path('like/<int:post_id>', views.handle_like, name='like'),
    path('follow/<int:user_id>', views.handle_follow, name='follow'),
    path('repost/<int:post_id>', views.handle_repost, name='repost'),
    path('comment/<int:post_id>', views.handle_comment, name='comment'),
]
