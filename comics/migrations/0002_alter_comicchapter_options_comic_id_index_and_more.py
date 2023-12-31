# Generated by Django 4.0.10 on 2023-10-14 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comicchapter',
            options={'ordering': ['chapter']},
        ),
        migrations.AddIndex(
            model_name='comic',
            index=models.Index(fields=['id'], name='id_index'),
        ),
        migrations.AddIndex(
            model_name='comicchapter',
            index=models.Index(fields=['comic', 'chapter'], name='comic_chapter_index'),
        ),
        migrations.AddIndex(
            model_name='comicpage',
            index=models.Index(fields=['chapter', 'page'], name='chapter_page_index'),
        ),
    ]
