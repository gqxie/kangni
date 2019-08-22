# Create your views here.
# encoding: utf-8
import datetime
import random

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, WordCloud, Line, Timeline, Bar3D, Grid


def index(request):
    context = {"bar": bar(), "line": line(), "pie_base": pie_base(), "timeline_bar": timeline_bar()}
    return render(request, 'log/pyecharts.html', context)


# def homePageBak(request):
#     context = {"bar3d_base": bar3d_base(), "grid_vertical": grid_vertical(),
#                "line_areastyle_boundary_gap": line_areastyle_boundary_gap(), "line_markline": line_markline()}
#     return render(request, 'log/homepage_bak.html', context)


def homePage(request):
    context = {}
    return render(request, 'log/homePage.html', context)


def vuePage(request):
    context = {}
    return render(request, 'log/vuepage.html', context)


def eventReport(request):
    context = {}
    return render(request, 'log/eventReport.html', context)


def getAllCamera(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    start = int(size) * (int(page) - 1)
    sql = '''SELECT
        rec.id,
        rec.`name` cameraName,
        rec.ip,
        DATE_FORMAT(
            rec.online_time,
            '%Y-%m-%d %H:%i:%S'
        ) onlineTime,
        DATE_FORMAT(
            rec.create_time,
            '%Y-%m-%d %H:%i:%S'
        ) createTime,
        recu.`name` cameraUseType
    FROM
        resource_camera rec
    LEFT JOIN resource_camerausetype recu ON rec.useType_id = recu.id limit {},{};'''

    sql = sql.format(start, size)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = []
    columns = ['id', 'cameraName', 'ip', 'onlineTime', 'createTime', 'cameraUseType']
    for row in rows:
        tmp_dict = {}
        for col in columns:
            tmp_dict[col] = row[columns.index(col)]
        online_time = tmp_dict['onlineTime']
        now = datetime.datetime.now()
        online_time = datetime.datetime.strptime(online_time, "%Y-%m-%d %H:%M:%S")
        duration = (now - online_time).seconds
        state = u'在线' if duration < 60 else u'离线'
        tmp_dict['state'] = state
        data_list.append(tmp_dict)

    count_sql = '''select count(1) from resource_camera;'''
    cursor.execute(count_sql)
    count = cursor.fetchone()[0]
    rst = {
        'count': count,
        'data': data_list
    }
    return JsonResponse(rst)


def getAllEventByCamera(request):
    rst = {}
    camera_id = request.GET.get('id')
    if None == camera_id:
        return JsonResponse(rst)
    start_date_time = request.GET.get('start')
    end_date_time = request.GET.get('end')
    criteria = ''
    search_by_time = len(start_date_time) > 0 and len(end_date_time) > 0
    if (search_by_time):
        start_date_time = '%s 00:00:00' % start_date_time
        end_date_time = '%s 23:59:59' % end_date_time
        criteria = ' and create_time > \'{}\' and create_time < \'{}\' '.format(start_date_time,
                                                                                end_date_time)
    cursor = connection.cursor()
    month_sql = 'select DISTINCT SUBSTR(create_time,1,7) months from resource_event  where camera_id = {} {} ORDER BY create_time desc ;'
    month_sql = month_sql.format(camera_id, criteria)
    cursor.execute(month_sql)
    month_rows = cursor.fetchall()
    months = [i[0] for i in month_rows]

    day_sql = 'select DISTINCT SUBSTR(create_time,1,10) days from resource_event  where camera_id = {} {} ORDER BY create_time desc ;'
    day_sql = day_sql.format(camera_id, criteria)
    cursor.execute(day_sql)
    day_rows = cursor.fetchall()
    days = [i[0] for i in day_rows]

    event_sql = 'select photo,SUBSTR(create_time,1,19) eventTime from resource_event where camera_id = {} {} order by create_time desc;'
    event_sql = event_sql.format(camera_id, criteria)
    cursor.execute(event_sql)
    event_rows = cursor.fetchall()

    url = ''
    if (len(event_rows) > 0):
        url = '%s%s%s' % (settings.DOMAIN_NAME, settings.MEDIA_URL, event_rows[0][0])

    month_dict = {}
    for month in months:
        month_dict[month] = {}

    for day in days:
        # 2019-08
        month_prefix = day[0:7]
        days_dict = month_dict[month_prefix]
        # 08-20
        days_dict[day[5:10]] = []
        month_dict[month_prefix] = days_dict

    srcList = []
    for row in event_rows:
        photo = '%s%s%s' % (settings.DOMAIN_NAME, settings.MEDIA_URL, row[0])
        event_time = row[1]
        srcList.append(photo)

        _month_prefix = event_time[0:7]
        _day_prefix = event_time[5:10]
        time_list = month_dict[_month_prefix][_day_prefix]
        time_item = {
            'label': event_time,
            'url': photo
        }
        time_list.append(time_item)
        month_dict[_month_prefix][_day_prefix] = time_list

    data = []
    for month_k, month_v in month_dict.items():

        day_list = []
        for day_k, day_v in month_v.items():
            item_list = []
            for item in day_v:
                item_list.append(item)
            day_item = {
                'label': day_k.replace('-', '月') + '日',
                'children': item_list
            }
            day_list.append(day_item)

        month_item = {
            'label': month_k.replace('-', '年') + '月',
            'children': day_list
        }
        data.append(month_item)
    rst = {
        'url': url,
        'data': data,
        'srcList': srcList
    }
    return JsonResponse(rst)


# 获取违章记录
def getPageEvent(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    start = int(size) * (int(page) - 1)
    start_date_time = request.GET.get('start')
    end_date_time = request.GET.get('end')
    cursor = connection.cursor()
    sql = """SELECT
        rev.id eventId,
        IFNULL(reem.`name`,'')employeName,
        reet.`name` eventType,
        reca.`name` cameraName,
        recat.`name` cameraUseType,
        redi.`name` districtName,
        repo.`name` positionName,
        rev.photo,
        DATE_FORMAT( rev.create_time, '%Y-%m-%d %H:%i:%S' ) createTime 
    FROM
        resource_event rev
        LEFT JOIN resource_eventtype reet ON rev.event_type_id = reet.id
        LEFT JOIN resource_camera reca ON rev.camera_id = reca.id
        LEFT JOIN resource_camerausetype recat ON reca.useType_id = recat.id
        LEFT JOIN resource_position repo ON reca.position_id = repo.id
        LEFT JOIN resource_district redi ON repo.district_id = redi.id 
        LEFT join resource_employe reem on rev.employe_id=reem.id 
        {}
    ORDER BY
        rev.update_time DESC limit {},{};"""

    criteria = ''
    search_by_time = len(start_date_time) > 0 and len(end_date_time) > 0
    if (search_by_time):
        criteria = ' where rev.create_time > \'{}\' and rev.create_time < \'{}\' '.format(start_date_time,
                                                                                          end_date_time)
    sql = sql.format(criteria, start, size)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = []
    columns = ['eventId', 'employeName', 'eventType', 'cameraName',
               'cameraUseType', 'districtName', 'positionName', 'photo', 'createTime']
    for row in rows:
        tmp_dict = {}
        for col in columns:
            tmp_dict[col] = row[columns.index(col)]
            if 'photo' == col:
                tmp_dict[col] = '%s%s%s' % (settings.DOMAIN_NAME, settings.MEDIA_URL, row[columns.index(col)])
        data_list.append(tmp_dict)

    count_sql = '''select count(1) from resource_event {};'''
    count_criteria = ''
    if (search_by_time):
        count_criteria = ' where create_time > \'{}\' and create_time < \'{}\' '.format(start_date_time, end_date_time)
    count_sql = count_sql.format(count_criteria)
    cursor.execute(count_sql)
    count = cursor.fetchone()[0]
    rst = {
        'count': count,
        'data': data_list
    }
    return JsonResponse(rst)


def getDataToExport(request):
    start_date_time = request.GET.get('start')
    end_date_time = request.GET.get('end')
    cursor = connection.cursor()
    sql = """SELECT
        rev.id eventId,
        IFNULL(reem.`name`,'')employeName,
        redi.`name` districtName,
        repo.`name` positionName,
        reet.`name` eventType,
        rev.photo,
        DATE_FORMAT( rev.create_time, '%Y-%m-%d %H:%i:%S' ) createTime 
    FROM
        resource_event rev
        LEFT JOIN resource_eventtype reet ON rev.event_type_id = reet.id
        LEFT JOIN resource_camera reca ON rev.camera_id = reca.id
        LEFT JOIN resource_camerausetype recat ON reca.useType_id = recat.id
        LEFT JOIN resource_position repo ON reca.position_id = repo.id
        LEFT JOIN resource_district redi ON repo.district_id = redi.id 
        LEFT join resource_employe reem on rev.employe_id=reem.id 
        {}
    ORDER BY
        rev.update_time DESC;"""

    criteria = ''
    search_by_time = len(start_date_time) > 0 and len(end_date_time) > 0
    if (search_by_time):
        criteria = ' where rev.create_time > \'{}\' and rev.create_time < \'{}\' '.format(start_date_time,
                                                                                          end_date_time)
    sql = sql.format(criteria)
    cursor.execute(sql)
    rows = cursor.fetchall()
    data_list = []
    columns = ['eventId', 'employeName', 'districtName', 'positionName', 'eventType', 'photo', 'createTime']
    for row in rows:
        tmp_dict = {}
        for col in columns:
            tmp_dict[col] = row[columns.index(col)]
            if 'photo' == col:
                tmp_dict[col] = '%s%s%s' % (settings.DOMAIN_NAME, settings.MEDIA_URL, row[columns.index(col)])
        data_list.append(tmp_dict)
    rst = {
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

    bar = Bar(init_opts=opts.InitOpts(height="350px"))
    bar.add_xaxis(name_list)
    for event_type in event_type_list:
        tmp_list = [0 for i in range(len(name_list))]
        for row in rows:
            if event_type == row[1]:
                index = name_list.index(row[0])
                tmp_list[index] = row[2]

        bar.add_yaxis(event_type, tmp_list)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="违章记录统计"), toolbox_opts=opts.ToolboxOpts(is_show=False,
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

    line = Line(init_opts=opts.InitOpts(height="350px"))
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
        Pie(init_opts=opts.InitOpts(height="350px"))
            .add("", rst)
            .set_global_opts(title_opts=opts.TitleOpts(title="违章记录占比"))
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

    tl = Timeline(init_opts=opts.InitOpts(height="350px"))

    for day in name_list:
        bar = Bar()
        bar.add_xaxis(['违章记录'])

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

# def bar3d_base():
#     data = [(i, j, random.randint(0, 12)) for i in range(6) for j in range(24)]
#     c = (Bar3D(init_opts=opts.InitOpts(height="350px"))
#         .add(
#         "",
#         [[d[1], d[0], d[2]] for d in data],
#         xaxis3d_opts=opts.Axis3DOpts(Faker.clock, type_="category"),
#         yaxis3d_opts=opts.Axis3DOpts(Faker.week_en, type_="category"),
#         zaxis3d_opts=opts.Axis3DOpts(type_="value"),
#     )
#         .set_global_opts(
#         visualmap_opts=opts.VisualMapOpts(max_=20),
#         title_opts=opts.TitleOpts(title="图表一"),
#     )
#     )
#     return c.render_embed()
#
#
# def grid_vertical() -> Grid:
#     bar = (
#         Bar()
#             .add_xaxis(Faker.choose())
#             .add_yaxis("商家A", Faker.values())
#             .add_yaxis("商家B", Faker.values())
#             .set_global_opts(title_opts=opts.TitleOpts(title="图表二"))
#     )
#     line = (
#         Line()
#             .add_xaxis(Faker.choose())
#             .add_yaxis("商家A", Faker.values())
#             .add_yaxis("商家B", Faker.values())
#             .set_global_opts(
#             title_opts=opts.TitleOpts(title="", pos_top="48%"),
#             legend_opts=opts.LegendOpts(pos_top="48%"),
#         )
#     )
#
#     grid = (
#         Grid(init_opts=opts.InitOpts(height="350px"))
#             .add(bar, grid_opts=opts.GridOpts(pos_bottom="60%"))
#             .add(line, grid_opts=opts.GridOpts(pos_top="60%"))
#     )
#     return grid.render_embed()
#
#
# def line_areastyle_boundary_gap() -> Line:
#     c = (
#         Line(init_opts=opts.InitOpts(height="350px"))
#             .add_xaxis(Faker.choose())
#             .add_yaxis("商家A", Faker.values(), is_smooth=True)
#             .add_yaxis("商家B", Faker.values(), is_smooth=True)
#             .set_series_opts(
#             areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
#             label_opts=opts.LabelOpts(is_show=False),
#         )
#             .set_global_opts(
#             title_opts=opts.TitleOpts(title="图表三"),
#             xaxis_opts=opts.AxisOpts(
#                 axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
#                 is_scale=False,
#                 boundary_gap=False,
#             ),
#         )
#     )
#     return c.render_embed()
#
#
# def line_markline() -> Line:
#     c1 = (
#         Line()
#             .add_xaxis(Faker.choose())
#             .add_yaxis("商家A", Faker.values(), is_smooth=True)
#             .add_yaxis("商家B", Faker.values(), is_smooth=True)
#             .set_series_opts(
#             areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
#             label_opts=opts.LabelOpts(is_show=False),
#         )
#             .set_global_opts(
#             title_opts=opts.TitleOpts(title="图表四"),
#             xaxis_opts=opts.AxisOpts(
#                 axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
#                 is_scale=False,
#                 boundary_gap=False,
#             ),
#         )
#     )
#
#     c2 = (
#         Line()
#             .add_xaxis(Faker.choose())
#             .add_yaxis(
#             "商家A",
#             Faker.values(),
#             markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
#         )
#             .add_yaxis(
#             "商家B",
#             Faker.values(),
#             markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
#         )
#             .set_global_opts(title_opts=opts.TitleOpts(title=""))
#     )
#
#     grid = (
#         Grid(init_opts=opts.InitOpts(height="350px"))
#             .add(c1, grid_opts=opts.GridOpts(pos_bottom="60%"))
#             .add(c2, grid_opts=opts.GridOpts(pos_top="60%"))
#     )
#     return grid.render_embed()
