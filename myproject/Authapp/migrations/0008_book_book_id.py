# Generated by Django 3.2.10 on 2024-01-26 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authapp', '0007_remove_book_book_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_id',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
