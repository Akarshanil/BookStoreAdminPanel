# Generated by Django 3.2.10 on 2024-01-26 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
