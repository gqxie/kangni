import logging
import logging
import os
import random

from django.conf import settings
from django.http import JsonResponse
# Create your views here.
from django.utils import timezone
from django.views.decorators.http import require_POST

from resource.models import Event, Camera, EventType, Position

logger = logging.getLogger(__name__)


@require_POST
def addEvent(request):
    msg = '添加违章记录失败！'
    status = -1
    rst = {
        'status': status,
        'msg': msg
    }
    data = request.FILES.get('file', None)
    if data is None:
        rst['msg'] = '文件不存在!'
        return JsonResponse(rst)
    # 转bytes类型
    try:
        pic = data.read()
        # 生成 随机文件名字
        now_time = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = "%06d" % random.randint(0, 999999)
        name = now_time + random_str
        fname = "{}.png".format(name)

        directory = os.path.join(settings.MEDIA_ROOT, 'events', timezone.now().strftime('%Y-%m-%d'))
        if not os.path.exists(directory):
            os.mkdir(directory)
        pic_path = os.path.join(directory, fname)
        with open(pic_path, 'wb+') as f:
            f.write(pic)

        camera_id = request.POST.get('cameraId')
        event_type_id = request.POST.get('eventTypeId')
        position_id = request.POST.get('positionId')
        photo = os.path.join('events', timezone.now().strftime('%Y-%m-%d'), fname)
        photo_height = request.POST.get('photoHeight')
        photo_weight = request.POST.get('photoWeight')

        try:
            camera = Camera.objects.get(pk=camera_id)
        except Camera.DoesNotExist:
            msg = '摄像头不存在！'
            rst['msg'] = msg
            logger.error(msg)
            return JsonResponse(rst)

        try:
            event_type = EventType.objects.get(pk=event_type_id)
        except EventType.DoesNotExist:
            msg = '违章记录不存在！'
            rst['msg'] = msg
            logger.error(msg)
            return JsonResponse(rst)
        
        try:
            postion = Position.objects.get(pk=position_id)
        except Position.DoesNotExist:
            msg = '作业单位不存在！'
            rst['msg'] = msg
            logger.error(msg)
            return JsonResponse(rst)

        event = Event(event_type=event_type, camera=camera, photo=photo,position=postion, photo_height=photo_height,
                      photo_width=photo_weight)
        event.save()
    except Exception as e:
        logger.error('添加违章记录失败！', e)
        return JsonResponse(rst)

    rst = {
        'status': 0,
        'msg': '添加违章记录成功！',
        'pic_path': pic_path
    }
    logger.info('添加违章记录成功，图片路径：%s' % pic_path)
    return JsonResponse(rst)
