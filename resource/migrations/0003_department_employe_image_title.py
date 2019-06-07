# Generated by Django 2.2.2 on 2019-06-05 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0002_remove_camera_enable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='一个部门的名字应该唯一', max_length=128, unique=True, verbose_name='部门名')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门管理',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='职务')),
            ],
            options={
                'verbose_name': '职务',
                'verbose_name_plural': '职务管理',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='图片')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Title')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片管理',
            },
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='员工的名字', max_length=128, verbose_name='名称')),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('idCard', models.CharField(blank=True, help_text='18位的身份证号码', max_length=18, null=True, verbose_name='身份证号')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('birthday', models.DateField(verbose_name='生日')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Department', verbose_name='部门')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Title', verbose_name='职务')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工管理',
            },
        ),
    ]
