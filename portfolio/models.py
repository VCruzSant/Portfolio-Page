import string
from random import SystemRandom

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django_summernote.models import AbstractAttachment

from utils.resizer import resize_image

# Create your models here.

# title description slug
# is_published
# cover
# category (Relação)
# Author (Relação)


class ProjectAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name

        if file_changed:
            resize_image(self.file)

        return super_save


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class ProjectManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True) \
            .order_by('-id') \
            .select_related('category', 'author')


class Project(models.Model):
    objects = ProjectManager()
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    detail_project = models.TextField()
    link = models.CharField(max_length=65, blank=True, default='')
    link_git = models.CharField(max_length=65, blank=True, default='')
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='project/covers/%Y/%m/%d', blank=True, default=''
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits, k=5
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                resize_image(self.cover)
            except FileNotFoundError:
                ...

        return saved


class Portfolio(models.Model):
    photo = models.ImageField(
        upload_to='project/photo/%Y/%m/%d', blank=True, default=''
    )
