# -*- coding: utf-8 -*-
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap

from pymongo import MongoClient

app = Flask(__name__)

bootstrap = Bootstrap()
bootstrap.init_app(app)


#@app.route('/')
#def hello_world():
#    return render_template('index.html')
client = MongoClient('172.17.0.2', 27017)
result = client['zhaopin']['result'].find_one({})['result']
res = {
    'title': {
        'text': '全国各城市职位数量'
    },
    'tooltip': {},
    'legend': {
        'data': ['职位数']
    },
    'xAxis': {
        'data': list(result.keys())
    },
    'yAxis': {},
    'series': [{
        'name': '职位数',
        'type': 'bar',
        'data': list(result.values())
    }]
}


@app.route('/data')
def vue():
    return jsonify(res)

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')