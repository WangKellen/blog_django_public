import os
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from mdeditor.fields import MDTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.move import file_move_safe
from uuslug import uuslug

class BlogPostManager(models.Manager):
    def filter_by_category_and_tag(self, category_name=None, tag_name=None):
        """
        根据分类和标签过滤文章
        """
        queryset = self.get_queryset()

        if category_name and category_name != '全部':
            queryset = queryset.filter(category__name=category_name)

        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)

        return queryset

def cover_image_upload_path(instance, filename):
    """
    自定义图片上传路径，根据文章的 id 创建文件夹
    """
    if instance.id is None:
        # 如果文章还没有保存，id 为 None，暂时保存到一个临时文件夹
        return os.path.join('blog_covers', 'temp', filename)
    else:
        # 文章已经保存，根据 id 创建文件夹
        return os.path.join('blog_covers', str(instance.id), filename)

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    publish_date = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    cover_image = models.ImageField(upload_to=cover_image_upload_path, verbose_name='封面图片')
    content = MDTextField(verbose_name='内容')
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL, verbose_name='分类')
    tags = models.ManyToManyField('Tag', verbose_name='标签')

    objects = BlogPostManager()  # 使用自定义管理器，并确保属性名为 objects

    class Meta:
        db_table = '博客文章'
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

@receiver(post_save, sender=BlogPost)
def move_cover_image(sender, instance, created, **kwargs):
    if created and instance.cover_image:
        old_path = instance.cover_image.path
        new_path = instance.cover_image.storage.path(cover_image_upload_path(instance, instance.cover_image.name))

        # 创建新的文件夹
        new_folder = os.path.dirname(new_path)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)

        # 移动文件
        file_move_safe(old_path, new_path)

        # 更新文件路径
        instance.cover_image.name = cover_image_upload_path(instance, instance.cover_image.name)
        instance.save()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称', db_index=True)
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL别名')  # 添加 slug 字段

    class Meta:
        db_table = '文章分类'
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        自动为 slug 字段生成值（基于 name 字段）
        """
        if not self.slug:  # 如果 slug 为空，则自动生成
            self.slug = uuslug(self.name, instance=self, max_length=100)
        super().save(*args, **kwargs)

    @property
    def post_count(self):
        """
        返回该分类关联的文章数量
        """
        return self.blogpost_set.count()

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='标签名称', db_index=True)

    class Meta:
        db_table = '文章标签'
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'

    def __str__(self):
        return self.name

    @property
    def post_count(self):
        """
        返回该标签关联的文章数量
        """
        return self.blogpost_set.count()
