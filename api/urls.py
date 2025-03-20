from django.urls import path
from .views import your_data, BlogPostList, TagList, BlogPostDetail

urlpatterns = [
    path('your-data/', your_data, name='hello'),
    path('blog-posts/',BlogPostList.as_view(),name='blog-post-list'),
    path('tags/', TagList.as_view(), name='tag-list'),
    path('blog-posts/<int:pk>/',BlogPostDetail.as_view(),name='blog-post-detail')
]