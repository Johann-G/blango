# Generated by Django 5.0.6 on 2024-06-07 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_rename_author_comment_creator_comment_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
