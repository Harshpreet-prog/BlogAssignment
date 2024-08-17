from django.contrib import admin
from .models import Blog, Tag, Comment, Like

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at', 'tags')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)  # If you want to use a more user-friendly interface for ManyToMany fields

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'created_at')
    search_fields = ('content', 'user__username', 'blog__title')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'blog')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'created_at')
    search_fields = ('comment__content', 'user__username')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'comment')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    