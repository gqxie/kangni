from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class District(models.Model):
    name = models.CharField(max_length=128, verbose_name='区域名称', help_text='区域名称应该唯一', unique=True, db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "区域"
        verbose_name_plural = "区域"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=128, verbose_name='安装位置', help_text='一个区域包含多个位置', unique=False, db_index=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='区域',
                                 db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "安装位置"
        verbose_name_plural = "安装位置"
        unique_together = (('name', 'district'),)

    def __str__(self):
        return '%s %s' % (self.district.name,self.name)


class CameraUseType(models.Model):
    name = models.CharField(max_length=128, verbose_name='摄像头用途', help_text='如人脸检测', unique=True, db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "摄像头用途"
        verbose_name_plural = "摄像头用途"

    def __str__(self):
        return self.name


class Camera(models.Model):
    name = models.CharField(max_length=128, verbose_name='名称', help_text='摄像头名称', null=False, blank=False,
                            db_index=True)
    useType = models.ForeignKey(CameraUseType, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='用途',
                                db_index=True)
    ip = models.CharField(max_length=100, verbose_name='ip地址', help_text='摄像头的ip地址', blank=True, null=True)
    username = models.CharField(max_length=128, verbose_name='用户名', help_text='摄像头连接用户名', null=False, default='',
                                blank=False,
                                db_index=True)
    password = models.CharField(max_length=128, verbose_name='密码', help_text='摄像头连接密码', null=False, default='',
                                blank=False,
                                db_index=True)
    address = models.ForeignKey(Position, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='安装地点',
                                db_index=True)
    online_time = models.DateTimeField(verbose_name='在线时间', default=timezone.now)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "摄像头"
        verbose_name_plural = "摄像头"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=128, verbose_name='部门名', help_text='一个部门的名字应该唯一', unique=True, db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门"

    def __str__(self):
        return self.name


class EventType(models.Model):
    name = models.CharField(max_length=128, verbose_name='事件类型名称', help_text='事件类型名称，如跨越围栏等', unique=True,
                            db_index=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "事件类型"
        verbose_name_plural = "事件类型"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=128, verbose_name='职务', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = '职务'
        verbose_name_plural = '职务'

    def get_absolute_url(self):
        return reverse('title-detail-view', args=(self.name,))

    def __str__(self):
        return self.name


class Employe(models.Model):
    name = models.CharField(max_length=128, verbose_name='姓名', help_text='员工的名字', null=False, blank=False,
                            db_index=True)

    gender_choices = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(choices=gender_choices, verbose_name='性别', blank=True, null=True)
    idCard = models.CharField(max_length=18, verbose_name='身份证号', help_text='18位的身份证号码', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='手机号',blank=True, null=True)
    birthday = models.DateField(verbose_name='生日',default='1900-01-01')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='部门',
                                   db_index=True)

    title = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='职务',
                              db_index=True)
    photo_height = models.PositiveIntegerField(blank=True, verbose_name='高度', default=0, null=True)
    photo_width = models.PositiveIntegerField(blank=True, verbose_name='宽度', default=0, null=True)
    photo = models.ImageField(upload_to="photos/%Y-%m-%d/", height_field='photo_height', verbose_name='照片',
                              width_field='photo_width',
                              default='default.png',blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "员工"
        verbose_name_plural = "员工"

    def __str__(self):
        return self.name


class Event(models.Model):
    # employe = models.ForeignKey(Employe, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='员工姓名',
    #                             db_index=True)
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='事件类型',
                                   db_index=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='摄像头',
                               db_index=True)
    photo_height = models.PositiveIntegerField(blank=True, verbose_name='高度', default=0)
    photo_width = models.PositiveIntegerField(blank=True, verbose_name='宽度', default=0)
    photo = models.ImageField(upload_to="events/%Y-%m-%d/", height_field='photo_height', verbose_name='照片',
                              width_field='photo_width',
                              default='event.png')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"

    def __str__(self):
        return self.employe.name
