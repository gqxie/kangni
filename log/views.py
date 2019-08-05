# Create your views here.

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
    rst = {
        'code': 0,
        'msg': '',
        'count': 1000,
        'data': [
            {
                'id': 10000,
                'username': 'user-0',
                'sex': '女',
                'city': '城市-0',
                'sign': '签名-0',
                'experience': 255,
                'logins': 24,
                'wealth': 82830700,
                'classify': '作家',
                'score': 57
            },
            {
                'id': 10001,
                'username': 'user-1',
                'sex': '男',
                'city': '城市-1',
                'sign': '签名-1',
                'experience': 884,
                'logins': 58,
                'wealth': 64928690,
                'classify': '词人',
                'score': 27
            },
            {
                'id': 10002,
                'username': 'user-2',
                'sex': '女',
                'city': '城市-2',
                'sign': '签名-2',
                'experience': 650,
                'logins': 77,
                'wealth': 6298078,
                'classify': '酱油',
                'score': 31
            },
            {
                'id': 10003,
                'username': 'user-3',
                'sex': '女',
                'city': '城市-3',
                'sign': '签名-3',
                'experience': 362,
                'logins': 157,
                'wealth': 37117017,
                'classify': '诗人',
                'score': 68
            },
            {
                'id': 10004,
                'username': 'user-4',
                'sex': '男',
                'city': '城市-4',
                'sign': '签名-4',
                'experience': 807,
                'logins': 51,
                'wealth': 76263262,
                'classify': '作家',
                'score': 6
            },
            {
                'id': 10005,
                'username': 'user-5',
                'sex': '女',
                'city': '城市-5',
                'sign': '签名-5',
                'experience': 173,
                'logins': 68,
                'wealth': 60344147,
                'classify': '作家',
                'score': 87
            },
            {
                'id': 10006,
                'username': 'user-6',
                'sex': '女',
                'city': '城市-6',
                'sign': '签名-6',
                'experience': 982,
                'logins': 37,
                'wealth': 57768166,
                'classify': '作家',
                'score': 34
            },
            {
                'id': 10007,
                'username': 'user-7',
                'sex': '男',
                'city': '城市-7',
                'sign': '签名-7',
                'experience': 727,
                'logins': 150,
                'wealth': 82030578,
                'classify': '作家',
                'score': 28
            },
            {
                'id': 10008,
                'username': 'user-8',
                'sex': '男',
                'city': '城市-8',
                'sign': '签名-8',
                'experience': 951,
                'logins': 133,
                'wealth': 16503371,
                'classify': '词人',
                'score': 14
            },
            {
                'id': 10009,
                'username': 'user-9',
                'sex': '女',
                'city': '城市-9',
                'sign': '签名-9',
                'experience': 484,
                'logins': 25,
                'wealth': 86801934,
                'classify': '词人',
                'score': 75
            }
        ]
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
