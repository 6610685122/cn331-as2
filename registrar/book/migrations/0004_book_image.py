# Generated by Django 5.1.1 on 2024-10-06 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_author_options_alter_book_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='upload'),
        ),
    ]