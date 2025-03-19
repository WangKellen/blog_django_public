# blog/admin.py

from django.contrib import admin
from .models import BlogPost, Category, Tag
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')  # 确保 slug 是模型中的字段
    search_fields = ('name',)  # 添加搜索功能
    prepopulated_fields = {'slug': ('name',)}  # 自动生成 slug 字段

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post_count')  # 添加 post_count 字段
    search_fields = ('name',)  # 添加搜索功能

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cover_image_preview', 'publish_date', 'category')
    list_filter = ('publish_date', 'category', 'tags')  # 添加分类和标签过滤
    ordering = ('-publish_date',)
    filter_horizontal = ('tags',)  # 提供更好的多对多选择界面

    def cover_image_preview(self, obj):
        """
        显示封面图片的预览
        """
        if obj.cover_image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.cover_image.url)
        return "无封面图片"
    cover_image_preview.short_description = '封面图片'

# 注册模型和自定义的 ModelAdmin 类
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
