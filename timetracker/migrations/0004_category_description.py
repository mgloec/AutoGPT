# Generated by Django 5.1.5 on 2025-01-26 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetracker', '0003_category_alter_task_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
