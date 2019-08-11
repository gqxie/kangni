import datetime
import time

from django.contrib import admin

# Register your models here.
from django.utils import timezone
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from resource.models import Camera, Department, Title, Employe, District, Position, CameraUseType, EventType, Event


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    search_fields = ('name',)
    list_per_page = 10
    actions_on_top = True


class ProxyResource(resources.ModelResource):
    class Meta:
        model = Camera


@admin.register(Camera)
class CameraAdmin(ImportExportActionModelAdmin):
    def district(self, obj):
        return obj.position.district.name

    district.short_description = u'作业场所'

    def full_online_time(self, obj):
        return obj.online_time.strftime("%Y-%m-%d %H:%M:%S")

    full_online_time.short_description = u'在线时间'

    def full_create_time(self, obj):
        return obj.create_time.strftime("%Y-%m-%d %H:%M:%S")

    full_create_time.short_description = u'创建时间'

    def state(self, obj):
        online_time = obj.online_time
        now = timezone.now()
        duration = (now - online_time).seconds
        state = u'在线' if duration < 60 else u'离线'
        color = 'green' if state == u'在线' else 'red'
        rst = mark_safe('<div style="color:%s" width="50px">%s</div>' % (color, state))
        return rst

    state.short_description = u'状态'
    resource_class = ProxyResource
    list_display = (
        'id', 'name', 'useType', 'ip', 'username', 'password', 'district','state', 'full_online_time',
        'full_create_time')
    search_fields = ('name', 'useType')
    list_per_page = 10
    list_filter = ('useType', 'create_time')
    list_display_links = ('name',)
    list_editable = ('useType',)


class EmployeResource(resources.ModelResource):
    class Meta:
        model = Employe


class AgeListFilter(admin.SimpleListFilter):
    title = u'最近生日'
    parameter_name = 'ages'

    def lookups(self, request, model_admin):
        return (
            ('0', u'最近7天'),
            ('1', u'最近15天'),
            ('2', u'最近30天'),
        )

    def queryset(self, request, queryset):
        # 当前日期格式
        cur_date = datetime.datetime.now().date()
        if self.value() == '0':
            day = cur_date - datetime.timedelta(days=7)
            return queryset.filter(birthday__gte=day)
        if self.value() == '1':
            day = cur_date - datetime.timedelta(days=15)
            return queryset.filter(birthday__gte=day)
        if self.value() == '2':
            day = cur_date - datetime.timedelta(days=30)
            return queryset.filter(birthday__gte=day)


@admin.register(Employe)
class EmployeAdmin(ImportExportActionModelAdmin):
    resource_class = EmployeResource

    def upload_img(self, obj):
        try:
            img = mark_safe('<img src="%s" width="50px" />' % (obj.photo.url,))
        except Exception as e:
            img = ''
        return img

    upload_img.short_description = u'头像'
    upload_img.allow_tags = True
    readonly_fields = ['upload_img']
    list_display = ('id', 'name', 'gender', 'phone', 'birthday', 'department', 'title', 'upload_img', 'create_time')
    search_fields = ('name', 'idCard', 'department')
    list_per_page = 10
    raw_id_fields = ('department', 'title')
    list_filter = ('department', AgeListFilter)
    list_display_links = ('name',)
    list_editable = ('gender',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    search_fields = ('name',)
    list_per_page = 10
    list_display_links = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district', 'create_time')
    search_fields = ('name', 'district')
    list_per_page = 10
    list_display_links = ('name',)
    list_filter = ('district',)
    list_editable = ('district',)


@admin.register(CameraUseType)
class CameraUseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    search_fields = ('name',)
    list_per_page = 10
    list_display_links = ('name',)


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_time')
    search_fields = ('name',)
    list_per_page = 10
    list_display_links = ('name',)


class EventResource(resources.ModelResource):
    class Meta:
        model = Event


@admin.register(Event)
class EventAdmin(ImportExportActionModelAdmin):

    def district(self, obj):
        return obj.camera.position.district.name

    district.short_description = u'作业场所'

    def position(self, obj):
        return obj.camera.position.name

    position.short_description = u'作业单位'

    def upload_img(self, obj):
        try:
            img = mark_safe('<img src="%s" width="50px" />' % (obj.photo.url,))
        except Exception as e:
            img = ''
        return img

    def full_create_time(self, obj):
        return obj.create_time.strftime("%Y-%m-%d %H:%M:%S")

    full_create_time.short_description = u'违章时间'

    upload_img.short_description = u'照片'
    upload_img.allow_tags = True
    readonly_fields = ['upload_img']
    resource_class = EventResource
    list_display = ('id', 'employe','event_type', 'district', 'position', 'camera', 'upload_img', 'full_create_time')
    list_per_page = 10
    list_display_links = ('id',)
    list_filter = ('event_type', 'camera','employe')
    list_editable = ('event_type', 'camera','employe')
