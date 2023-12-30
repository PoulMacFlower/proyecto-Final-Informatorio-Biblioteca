# Generated by Django 5.0 on 2023-12-29 02:39

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', ckeditor.fields.RichTextField()),
                ('image', models.ImageField(upload_to='articles/images')),
                ('date_published', models.DateField(default=datetime.date.today)),
            ],
        ),
    ]
