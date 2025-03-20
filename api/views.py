from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import BlogPost, Category, Tag
from rest_framework import generics
from rest_framework import serializers

class BlogPostSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(many=True)
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'publish_date', 'cover_image', 'content', 'category', 'tags']

class BlogPostList(generics.ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        # 获取查询参数
        category_name = self.request.query_params.get('category', '全部')
        tag_name = self.request.query_params.get('tag')
        limit = self.request.query_params.get('limit')  # 默认不限制数量

        # 过滤文章并按发布时间倒序排序
        queryset = BlogPost.objects.filter_by_category_and_tag(category_name, tag_name)
        queryset = queryset.order_by('-publish_date')  # 按发布日期的倒序排序

        # 如果 limit 参数存在，则限制返回数量
        if limit:
            queryset = queryset[:int(limit)]

        return queryset
def your_data(request):
    data = {
        'text': '这是从 API 获取的内容'
    }
    return JsonResponse(data)


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField( read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'post_count']

class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

# views.py

class BlogPostDetail(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
