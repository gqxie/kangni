# Create your views here.
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Geo, Gauge, Pie, WordCloud


def index(request):
    context = {"bar": bar(), "geo": geo(), "pie_base": pie_base(), "gauge_base": gauge_base()}
    return render(request, 'log/pyecharts.html', context)


def layui(request):
    context = {}
    return render(request, 'log/layui.html', context)


def getUser(request):
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    start = int(limit) * (int(page) - 1)
    cursor = connection.cursor()
    sql = """SELECT
            rev.id eventId,
            reet.`name` eventType,
            reem.`name` employeName,
            CASE
        WHEN reem.gender = 1 THEN
            '男'
        WHEN reem.gender = 2 THEN
            '女'
        ELSE
            '未知'
        END gender,
         rede.`name` departmentName,
         reti.`name` titleName,
         reca.`name` cameraName,
         recat.`name` cameraUseType,
         redi.`name` districtName,
         repo.`name` positionName,
         rev.photo,
        DATE_FORMAT(rev.create_time, '%Y-%m-%d %H:%i:%S') createTime
        FROM
            resource_event rev
        LEFT JOIN resource_employe reem ON rev.employe_id = reem.id
        LEFT JOIN resource_department rede ON reem.department_id = rede.id
        LEFT JOIN resource_title reti ON reem.title_id = reti.id
        LEFT JOIN resource_eventtype reet ON rev.event_type_id = reet.id
        LEFT JOIN resource_camera reca ON rev.camera_id = reca.id
        LEFT JOIN resource_camerausetype recat ON reca.useType_id = recat.id
        LEFT JOIN resource_position repo ON reca.address_id = repo.id
        LEFT JOIN resource_district redi ON repo.district_id = redi.id
        ORDER BY
            rev.update_time DESC limit {},{};"""
    sql = sql.format(start, limit)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = []
    columns = ['eventId', 'eventType', 'employeName', 'gender', 'departmentName', 'titleName', 'cameraName',
               'cameraUseType', 'districtName', 'positionName', 'photo', 'createTime']
    for row in rows:
        tmp_dict = {}
        for col in columns:
            tmp_dict[col] = row[columns.index(col)]
            if 'photo' == col:
                tmp_dict[col] = '%s%s%s' % (settings.DOMAIN_NAME, settings.MEDIA_URL, row[columns.index(col)])
        data_list.append(tmp_dict)

    count_sql = 'select count(1) from resource_event;'
    cursor.execute(count_sql)
    count = cursor.fetchone()[0]
    rst = {
        'code': 0,
        'msg': '',
        'count': count,
        'data': data_list
    }
    return JsonResponse(rst)


def bar():
    cursor = connection.cursor()
    cursor.execute("""select rem.`name`,revt.`name` eventType,count(*) cnt from resource_event rev LEFT JOIN
        resource_employe rem on rev.employe_id = rem.id 
        LEFT JOIN resource_eventtype revt on rev.event_type_id = revt.id
        GROUP BY employe_id,event_type_id;""")
    rows = cursor.fetchall()
    name_list = []
    event_type_list = []
    for row in rows:
        name = row[0]
        if name not in name_list:
            name_list.append(name)
        event_type = row[1]
        if event_type not in event_type_list:
            event_type_list.append(event_type)

    bar = Bar()
    bar.add_xaxis(name_list)
    for event_type in event_type_list:
        tmp_list = [0 for i in range(len(name_list))]
        for row in rows:
            if event_type == row[1]:
                index = name_list.index(row[0])
                tmp_list[index] = row[2]

        bar.add_yaxis(event_type, tmp_list)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="不规范行为统计"), toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                                                                  feature=opts.ToolBoxFeatureOpts(
                                                                                                      restore=None,
                                                                                                      data_zoom=None)))
    return bar.render_embed()


def geo() -> Geo:
    c = (
        Geo()
            .add_schema(maptype="china")
            .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True),
            title_opts=opts.TitleOpts(title="Geo-VisualMap（分段型）"),
        )
    )
    return c.render_embed()


def pie_base() -> Pie:
    c = (
        Pie()
            .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c.render_embed()


def gauge_base() -> Gauge:
    c = (
        Gauge()
            .add("", [("完成率", 66.6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Gauge-基本示例"))
    )
    return c.render_embed()


def wc():
    myWordCloud = WordCloud("绘制词云", width=1000, height=620)
    name = ['Sam S Club', 'Macys', 'Amy Schumer', 'Jurassic World',
            'Charter Communications', 'Chick Fil A', 'Planet Fitness', 'Pitch Perfect',
            'Express', 'Home', 'Johnny Depp', 'Lena Dunham',
            'Lewis Hamilton', 'KXAN', 'Mary Ellen Mark', 'Farrah Abraham',
            'Rita Ora', 'Serena Williams', 'NCAA baseball tournament', 'Point Break']
    value = [10000, 6181, 4386, 4055, 2467, 2244, 1898, 1484, 1112, 965,
             847, 582, 555, 550, 462, 366, 360, 282, 273, 265]
    myWordCloud.add("", name, value, word_size_range=[20, 100])
    return myWordCloud.render_embed()
