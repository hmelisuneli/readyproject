from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse


class Support(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=False, verbose_name="Content")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Photo url", null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Time create")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Time update")
    is_published = models.BooleanField(default=True, verbose_name="Publication")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name="Category")
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']
