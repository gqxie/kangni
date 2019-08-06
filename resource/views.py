import json
import os
import random

from django.conf import settings
from django.http import JsonResponse

# Create your views here.
from django.utils import timezone
from django.views.decorators.http import require_POST

from resource.models import Event, Employe, Camera, EventType


@require_POST
def addEvent(request):
    rst = {
        'status': -1,
        'msg': 'failed'
    }
    data = request.FILES.get('file', None)
    if data is None:
        return JsonResponse(rst)
    # 转bytes类型
    pic = data.read()
    pic_path = ''
    # 生成 随机文件名字
    now_time = timezone.now().strftime('%Y%m%d%H%M%S')
    random_str = "%06d" % random.randint(0, 999999)
    name = now_time + random_str
    fname = "{}.png".format(name)
    try:
        directory = os.path.join(settings.MEDIA_ROOT, 'events', timezone.now().strftime('%Y-%m-%d'))
        if not os.path.exists(directory):
            os.mkdir(directory)
        pic_path = os.path.join(directory, fname)
        with open(pic_path, 'wb+') as f:
            f.write(pic)
    except Exception as e:
        print('保存图片失败:' + str(e))

    try:
        employ_id = request.POST.get('employId')
        camera_id = request.POST.get('cameraId')
        event_type_id = request.POST.get('eventTypeId')
        photo = os.path.join('events', timezone.now().strftime('%Y-%m-%d'), fname)
        photo_height = request.POST.get('photoHeight')
        photo_weight = request.POST.get('photoWeight')

        employ = Employe.objects.get(pk=employ_id)
        camera = Camera.objects.get(pk=camera_id)
        event_type = EventType.objects.get(pk=event_type_id)

        event = Event(employe=employ, event_type=event_type, camera=camera, photo=photo, photo_height=photo_height,
                      photo_width=photo_weight)
        event.save()
    except Exception as e:
        return JsonResponse(rst)

    rst = {
        'status': 0,
        'msg': 'success',
        'pic_path': pic_path
    }
    return JsonResponse(rst)
