# Generated by Django 2.2.2 on 2019-08-04 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0007_auto_20190804_2311'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='position',
            unique_together={('name', 'district')},
        ),
    ]
