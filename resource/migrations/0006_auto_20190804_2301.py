# Generated by Django 2.2.2 on 2019-08-04 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0005_auto_20190804_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='photo',
            field=models.ImageField(default='default.png', height_field='photo_height', upload_to='photos/%Y-%m-%d/', verbose_name='照片', width_field='photo_width'),
        ),
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(default='default.png', height_field='photo_height', upload_to='events/%Y-%m-%d/', verbose_name='照片', width_field='photo_width'),
        ),
    ]
