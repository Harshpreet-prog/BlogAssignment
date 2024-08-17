from django.db import connection
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Blog

@receiver(post_save, sender=Blog)
def update_search_index(sender, instance, **kwargs):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO blog_blog_fts (rowid, title, content)
        VALUES (?, ?, ?)
        ON CONFLICT(rowid) DO UPDATE SET
        title=excluded.title,
        content=excluded.content;
    """, [instance.id, instance.title, instance.content])

@receiver(post_delete, sender=Blog)
def delete_search_index(sender, instance, **kwargs):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM blog_blog_fts WHERE rowid = ?", [instance.id])
