# Generated by Django 2.2.2 on 2019-08-04 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0002_auto_20190804_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='name',
            new_name='employe',
        ),
    ]
