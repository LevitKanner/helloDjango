# Generated by Django 3.1.2 on 2020-10-20 10:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='imgFile',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='', verbose_name='image'),
            preserve_default=False,
        ),
    ]
