# Generated by Django 5.1.6 on 2025-03-14 06:01

import blog.models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
import mdeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='分类名称')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
                'db_table': '文章分类',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='标签名称')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
                'db_table': '文章标签',
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('cover_image', models.ImageField(upload_to=blog.models.cover_image_upload_path, verbose_name='封面图片')),
                ('content', mdeditor.fields.MDTextField(verbose_name='内容')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category', verbose_name='分类')),
                ('tags', models.ManyToManyField(to='blog.tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '博客文章',
                'verbose_name_plural': '博客文章',
                'db_table': '博客文章',
                'ordering': ['-publish_date'],
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
