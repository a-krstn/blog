from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']     # поля буду отображаться в админке
    list_filter = ['status', 'created', 'publish', 'author']            # поля, по которым можно фильтровать
    search_fields = ['title', 'body']                                   # поля, по которым можно выполнять поиск
    prepopulated_fields = {'slug': ('title',)}                          # автом-ое запол-ие поля slug по полю title
    raw_id_fields = ['author']                                          # поисковый виджет при создании нового поста
    date_hierarchy = 'publish'                                          # навигация по датам публикации постов
    ordering = ['status', 'publish']                                    # поля сортировки


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
