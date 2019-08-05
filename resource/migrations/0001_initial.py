# Generated by Django 2.2.2 on 2019-08-05 22:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='摄像头名称', max_length=128, verbose_name='名称')),
                ('ip', models.CharField(blank=True, help_text='摄像头的ip地址', max_length=100, null=True, verbose_name='ip地址')),
                ('username', models.CharField(db_index=True, default='', help_text='摄像头连接用户名', max_length=128, verbose_name='用户名')),
                ('password', models.CharField(db_index=True, default='', help_text='摄像头连接密码', max_length=128, verbose_name='密码')),
                ('online_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='在线时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '摄像头',
                'verbose_name_plural': '摄像头',
            },
        ),
        migrations.CreateModel(
            name='CameraUseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='如人脸检测', max_length=128, unique=True, verbose_name='摄像头用途')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '摄像头用途',
                'verbose_name_plural': '摄像头用途',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='一个部门的名字应该唯一', max_length=128, unique=True, verbose_name='部门名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='区域名称应该唯一', max_length=128, unique=True, verbose_name='区域名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '区域',
                'verbose_name_plural': '区域',
            },
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='员工的名字', max_length=128, verbose_name='姓名')),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('idCard', models.CharField(blank=True, help_text='18位的身份证号码', max_length=18, null=True, verbose_name='身份证号')),
                ('phone', models.CharField(max_length=11, verbose_name='手机号')),
                ('birthday', models.DateField(verbose_name='生日')),
                ('photo_height', models.PositiveIntegerField(blank=True, default=0, verbose_name='高度')),
                ('photo_width', models.PositiveIntegerField(blank=True, default=0, verbose_name='宽度')),
                ('photo', models.ImageField(default='default.png', height_field='photo_height', upload_to='photos/%Y-%m-%d/', verbose_name='照片', width_field='photo_width')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Department', verbose_name='部门')),
            ],
            options={
                'verbose_name': '员工',
                'verbose_name_plural': '员工',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='事件类型名称，如跨越围栏等', max_length=128, unique=True, verbose_name='事件类型名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '事件类型',
                'verbose_name_plural': '事件类型',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='职务')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '职务',
                'verbose_name_plural': '职务',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='一个区域包含多个位置', max_length=128, verbose_name='安装位置')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.District', verbose_name='区域')),
            ],
            options={
                'verbose_name': '安装位置',
                'verbose_name_plural': '安装位置',
                'unique_together': {('name', 'district')},
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_height', models.PositiveIntegerField(blank=True, default=0, verbose_name='高度')),
                ('photo_width', models.PositiveIntegerField(blank=True, default=0, verbose_name='宽度')),
                ('photo', models.ImageField(default='default.png', height_field='photo_height', upload_to='events/%Y-%m-%d/', verbose_name='照片', width_field='photo_width')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('camera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Camera', verbose_name='摄像头')),
                ('employe', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Employe', verbose_name='员工姓名')),
                ('event_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.EventType', verbose_name='事件类型')),
            ],
            options={
                'verbose_name': '事件',
                'verbose_name_plural': '事件',
            },
        ),
        migrations.AddField(
            model_name='employe',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Title', verbose_name='职务'),
        ),
        migrations.AddField(
            model_name='camera',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.Position', verbose_name='安装地点'),
        ),
        migrations.AddField(
            model_name='camera',
            name='useType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resource.CameraUseType', verbose_name='用途'),
        ),
    ]
