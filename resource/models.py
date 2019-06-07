from django.db import models


# Create your models here.
from django.urls import reverse


class Camera(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称', help_text='摄像头名称', null=False, blank=False,
                            db_index=True)
    use_type_choices = (
        (0, '未知'),
        (1, '人脸检测'),
        (2, '安全帽检测'),
        (3, '安全带检测'),
        (4, '跨越围栏动作检测'),
    )
    useType = models.IntegerField(choices=use_type_choices, verbose_name='用途', default=0)
    ip = models.CharField(max_length=100, verbose_name='ip地址', help_text='摄像头的ip地址', blank=True, null=True)
    address = models.CharField(max_length=50, verbose_name='安装地点')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "摄像头"
        verbose_name_plural = "摄像头管理"

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=128, verbose_name='部门名', help_text='一个部门的名字应该唯一', unique=True, db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门管理"

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(max_length=128, verbose_name='职务', null=True, blank=True)

    class Meta:
        verbose_name = '职务'
        verbose_name_plural = '职务管理'

    def get_absolute_url(self):
        return reverse('title-detail-view', args=(self.name,))

    def __str__(self):
        return self.name



class Employe(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称', help_text='员工的名字', null=False, blank=False,
                            db_index=True)

    gender_choices = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(choices=gender_choices, verbose_name='性别', default=0)
    idCard = models.CharField(max_length=18, verbose_name='身份证号', help_text='18位的身份证号码', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='手机号')
    birthday = models.DateField(verbose_name='生日')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='部门',
                                   db_index=True)

    title = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='职务',
                              db_index=True)
    photo_height = models.PositiveIntegerField(blank = True, default = 0)
    photo_width = models.PositiveIntegerField(blank = True, default = 0)
    photo = models.ImageField(upload_to="photos", height_field='photo_height', width_field='photo_width',default='default.png')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)

    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "员工"
        verbose_name_plural = "员工管理"

    def __str__(self):
        return self.name