from django.db import models

class Project(models.Model):
    title = models.CharField("标题", max_length=100)
    description = models.TextField("介绍")
    image = models.ImageField("图片", upload_to='project_images/')
    is_visible = models.BooleanField("是否展示", default=True)

    def __str__(self):
        return self.title
