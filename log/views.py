# Create your views here.

from django.shortcuts import render
from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Geo, Gauge, Pie, WordCloud


def index(request):
    context = {"bar": bar(), "geo": geo(), "pie_base": pie_base(), "gauge_base": gauge_base()}
    return render(request, 'log/pyecharts.html', context)


def bar():
    bar = (
        Bar()
            .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
            .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
            .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    )
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
