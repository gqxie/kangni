import datetime

from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from resource.models import Camera, Department, Title, Employe



@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
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
    resource_class = ProxyResource
    list_display = ('id', 'name', 'useType', 'ip', 'address', 'create_time')
    search_fields = ('name', 'useType', 'address')
    list_per_page = 10
    list_filter = ('useType', 'address', 'create_time')
    list_display_links = ('name',)
    list_editable = ('useType', 'ip', 'address')
    # date_hierarchy = 'create_time'


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
    list_display = ('id', 'name', 'gender', 'phone', 'birthday', 'department', 'title','upload_img', 'create_time')
    search_fields = ('name', 'idCard', 'department')
    list_per_page = 10
    raw_id_fields = ('department', 'title')
    list_filter = ('department', AgeListFilter)
    list_display_links = ('name',)
    list_editable = ('department', 'title', 'phone', 'birthday', 'gender')
