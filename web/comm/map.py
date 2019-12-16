from pyecharts.charts import Scatter, EffectScatter, BMap
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

from pymongo import MongoClient
import json

from .config import MAPTYPE, BAIDU_AK


def scattermap(data):
    jscode = """ 
        function (val) {
                return val[2]/15;
            }
     """

    bmap = (BMap().add_schema(baidu_ak=BAIDU_AK,
                              center=[104.114129, 37.550339],
                              zoom=5,
                              is_roam=False,
                              map_style={
                                  'styleJson': MAPTYPE
                              }).add('城市分布',
                              [
                                  list(x) for x in zip(
                                      data['content']['name'],
                                      data['content']['item'],
                                  )
                                ],
                                type_='scatter',
                                symbol_size=JsCode(jscode)

                              )
                              .add('top5',
                              [list(x) for x in zip(data['content']['name'][:5],data['content']['item'][:5])],
                              type_='effectScatter',
                              symbol_size=JsCode(jscode)
                              ).set_global_opts(title_opts=opts.TitleOpts(title='城市分布')).dump_options_with_quotes()
                              )
    
    return bmap



