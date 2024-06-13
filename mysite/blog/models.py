from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)   # авт. сохр-ие даты создания
    updated = models.DateTimeField(auto_now=True)       # авт. сохр-ие даты обновления
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)   # поле статуса поста блога
    objects = models.Manager()          # дефолтный менеджер
    published = PublishedManager()      # конкретно-прикладной менеджер
    tags = TaggableManager()

    class Meta:
        """Класс определяет метаданные модели"""
        ordering = ['-publish']                   # параметр сорт-ки
        indexes = [
            models.Index(fields=['-publish'])     # параметр индекс-ния
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """возвращает канонический URL-адрес объекта"""
        return reverse('blog:post_detail', args=[self.publish.day,
                                                 self.publish.month,
                                                 self.publish.year,
                                                 self.slug])      # reverse динамически формирует URL-адрес


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80, verbose_name='Имя')
    email = models.EmailField()
    body = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])  # параметр индекс-ния
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
