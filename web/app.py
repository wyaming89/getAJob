# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from pymongo import MongoClient
from pyecharts.charts import Bar, Pie, Geo, BMap
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import json

from comm.map import scattermap

app = Flask(__name__)


@app.route('/data')
def vue():
    client = MongoClient('172.17.0.2', 27017)
    result = client.zhaopin.result
    salary = result.find_one({'title': {'$eq': '工资分布'}})
    indu = result.find_one({'title': {'$eq': '行业分布'}})
    citys = result.find_one({'title': {'$eq': '城市分布'}})
    joblv = result.find_one({'title': {'$eq': '职级分布'}})
    jscode = """ 
        function (val) {
                return val[2]/100;
            }
     """
    chart1 = (Bar().add_xaxis(salary['content']['name']).add_yaxis(
        '', salary['content']['item'],
        category_gap=0).set_global_opts(title_opts=opts.TitleOpts(
            title='工资分布', pos_right='10%')).dump_options_with_quotes())
    chart2 = (Pie().add('', [
        list(x) for x in zip(indu['content']['name'], indu['content']['item'])
    ],
                        radius=['30%', '75%'],
                        center=['40%', '50%'],
                        rosetype='radius').set_global_opts(
                            title_opts=opts.TitleOpts(title='行业分布',
                                                      pos_right='10%'),
                            legend_opts=opts.LegendOpts(
                                is_show=False)).dump_options_with_quotes())
    chart3 = (Bar().add_xaxis(joblv['content']['name']).add_yaxis(
        '',
        joblv['content']['item']).set_global_opts(title_opts=opts.TitleOpts(
            title='职级分布', pos_right='10%')).dump_options_with_quotes())

    chart4 = (Geo().add_schema(maptype='china',
    is_roam=False, zoom=1
    ).add('职位数量', [
        list(x) for x in zip(
            citys['content']['name'],
            citys['content']['item'],
        )
    ]).set_series_opts(label_opts=opts.LabelOpts(is_show=False,
                                                 formatter="{b}:{c}"),
                       markpoint_opts=opts.MarkPointItem(
                           symbol_size=JsCode(jscode))).set_global_opts(
                               title_opts=opts.TitleOpts(
                                   title='城市分布')).dump_options_with_quotes()) 
    #chart4 = scattermap(citys)

    resdict = {
        'res': [
            json.loads(chart1),
            json.loads(chart2),
            json.loads(chart3),
            json.loads(chart4)
        ]
    }
    return jsonify(resdict)

@app.route('/datas/<param>')
def getdata(param):
    return '获得的参数：%s'%param

