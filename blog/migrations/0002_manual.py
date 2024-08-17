from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE VIRTUAL TABLE blog_blog_fts USING fts5(
                title, content, content='blog_blog', content_rowid='id'
            );
            INSERT INTO blog_blog_fts (rowid, title, content)
            SELECT id, title, content FROM blog_blog;
            """
        ),
    ]
