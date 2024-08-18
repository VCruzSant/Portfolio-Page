import os
import string
from PIL import Image
from random import SystemRandom

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from project import settings

# Create your models here.

# title description slug
# is_published
# cover
# category (Relação)
# Author (Relação)


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
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d', blank=True, default=''
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, default=None
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize(
            (new_width, new_height), Image.LANCZOS)  # type: ignore
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

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
                self.resize_image(self.cover)
            except FileNotFoundError:
                ...

        return saved
