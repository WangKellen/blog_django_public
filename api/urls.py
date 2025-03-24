from django.urls import path
from .views import BlogPostList, TagList, BlogPostDetail

urlpatterns = [
    path('blog-posts/',BlogPostList.as_view(),name='blog-post-list'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('blog-posts/<int:pk>/',BlogPostDetail.as_view(),name='blog-post-detail')
]