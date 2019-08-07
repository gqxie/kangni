# Create your views here.
# encoding: utf-8
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, WordCloud, Line, Timeline


def index(request):
    context = {"bar": bar(), "line": line(), "pie_base": pie_base(), "timeline_bar": timeline_bar()}
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
            reca.`name` cameraName,
            recat.`name` cameraUseType,
            redi.`name` districtName,
            repo.`name` positionName,
            rev.photo,
            DATE_FORMAT(
                rev.create_time,
                '%Y-%m-%d %H:%i:%S'
            ) createTime
        FROM
            resource_event rev
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
    columns = ['eventId', 'eventType', 'cameraName',
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
    cursor.execute("""SELECT
            DATE_FORMAT( rev.create_time, '%Y-%m-%d' ) create_time,
            revt.`name`,
            count( * ) 
        FROM
            resource_event rev
            LEFT JOIN resource_eventtype revt ON rev.event_type_id = revt.id 
        GROUP BY
            create_time,
            event_type_id""")
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
    bar.set_global_opts(title_opts=opts.TitleOpts(title="不规范行为统计"), toolbox_opts=opts.ToolboxOpts(is_show=False,
                                                                                                  feature=opts.ToolBoxFeatureOpts(
                                                                                                      restore=None,
                                                                                                      data_zoom=None)))
    return bar.render_embed()


def line():
    cursor = connection.cursor()
    cursor.execute("""SELECT
            DATE_FORMAT( rev.create_time, '%Y-%m-%d' ) create_time,
            revt.`name`,
            count( * ) 
        FROM
            resource_event rev
            LEFT JOIN resource_eventtype revt ON rev.event_type_id = revt.id 
        GROUP BY
            create_time,
            event_type_id""")
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

    line = Line()
    line.add_xaxis(name_list)
    for event_type in event_type_list:
        tmp_list = [0 for i in range(len(name_list))]
        for row in rows:
            if event_type == row[1]:
                index = name_list.index(row[0])
                tmp_list[index] = row[2]

        line.add_yaxis(event_type, tmp_list, is_smooth=True)
    line.set_global_opts(title_opts=opts.TitleOpts(title="数量变化统计"))
    return line.render_embed()


def pie_base():
    cursor = connection.cursor()
    cursor.execute("""SELECT
            revt.`name` eventType,
            count( * ) cnt 
        FROM
            resource_event rev
            LEFT JOIN resource_eventtype revt ON rev.event_type_id = revt.id 
        GROUP BY
            rev.event_type_id;""")
    rows = cursor.fetchall()
    rst = []
    for row in rows:
        tmp = []
        tmp.append(row[0])
        tmp.append(row[1])
        rst.append(tmp)
    c = (
        Pie()
            .add("", rst)
            .set_global_opts(title_opts=opts.TitleOpts(title="事件类型占比"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    return c.render_embed()


def timeline_bar():
    cursor = connection.cursor()
    cursor.execute("""SELECT
                DATE_FORMAT( rev.create_time, '%Y-%m-%d' ) create_time,
                revt.`name`,
                count( * )
            FROM
                resource_event rev
                LEFT JOIN resource_eventtype revt ON rev.event_type_id = revt.id
            GROUP BY
                create_time,
                event_type_id""")
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

    tl = Timeline()

    for day in name_list:
        bar = Bar()
        bar.add_xaxis(['不规范行为'])

        for i in range(len(event_type_list)):
            event_type_name = event_type_list[i]
            num = 0
            for row in rows:
                if day == row[0] and event_type_name == row[1]:
                    num = row[2]
                    break

            bar.add_yaxis(event_type_name, [num])

        bar.set_global_opts(title_opts=opts.TitleOpts("{}".format(day)))
        tl.add(bar, "{}".format(day))
    return tl.render_embed()


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
