# Generated by Django 5.1.4 on 2025-01-05 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangowebapp', '0002_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.TextField(),
        ),
    ]
