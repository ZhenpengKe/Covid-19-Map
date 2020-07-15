'''
@Author: Mario
@Date: 2020-07-13 15:32:34
@LastEditTime: 2020-07-15 11:53:02
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \Python--master\china.py
'''

import requests
from lxml import etree
import json
from pyecharts.charts import Map  # 0.1.9.4
from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode

class nCov_2019():
    def __init__(self):
        self.headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        self.url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    

    def parse_url(self):
        response = requests.get("https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5")
        list_json = json.loads(response.text)
        return list_json

    def getDataList(self,list_json):
        # 将data数据类型str转成dict，方便操作数据
        global false, null ,true
        false = null = true = ''
        jo = list_json['data']
        data = eval(jo)
        return data

    def main(self):
        list_json = self.parse_url()
        data = self.getDataList(list_json)
        return data

nCoV_2019 = nCov_2019()
data = nCoV_2019.main()

area = []
nowConfirm = []
confirm = []
dead = []
heal = []
for i in range(34):
    area.append(data['areaTree'][0]['children'][i]['name'])
    nowConfirm.append(data['areaTree'][0]['children'][i]['total']['nowConfirm'])
    confirm.append(data['areaTree'][0]['children'][i]['total']['confirm'])
    dead.append(data['areaTree'][0]['children'][i]['total']['dead'])
    heal.append(data['areaTree'][0]['children'][i]['total']['heal'])

# 将数据封装成['beijing',[325,923,9,589]]的形式，方便数据可视化
data_pair = []
for i in range(34):
    x =[]
    x.append(confirm[i])
    x.append(dead[i])
    x.append(heal[i])
    x.append(nowConfirm[i])
    data_pair.append(x)

testv = []
for i in range(34):
    testMap=[area[i],data_pair[i]]
    testv.append(testMap)

tool_js="""
        function(params){
            console.log(params.data);
            return params.name+':' + '<br/>'
                                    +'现存确诊人数: ' + params.data.value[3]+ '<br/>'
                                    +'累计确诊人数: ' + params.data.value[0] + '<br/>'
                                    +'死亡人数: ' + params.data.value[1]+ '<br/>'
                                    +'治愈人数: ' + params.data.value[2];
        }
"""

# 画图, pyecharts官方文档
c = (
    Map().add(
            series_name = "", 
            data_pair = testv,
            maptype="china",
            label_opts=opts.LabelOpts(is_show=True),
            is_map_symbol_show=False
        ).set_series_opts(label_opts=opts.LabelOpts(
            formatter="{b}"),
            rich={
                'b':{
                    'fontSize':14,
                    'color':'#fff',
                    'textBorderColor':'black',
                    'textBorderWidth':'0.5'
                    }
                }
            )
        .set_global_opts(title_opts=opts.TitleOpts(title="2020中国疫情地图", subtitle='Created by Mario'),
                        visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                            pieces=[
                                                                {"min":0,"max":0,"color":"#ffffff"},
                                                                {"min":1,"max":10,"color":"#ebb4a8"},
                                                                {"min":10,"max":100,"color":"#e09694"},
                                                                {"min":100,"max":500,"color":"#cb8382"},
                                                                {"min":500,"max":1000,"color":"#b27372"},
                                                                {"min":1000,"color":"#976461"},
                                                                ],is_inverse=True,pos_right=10),
                        tooltip_opts=opts.TooltipOpts(axis_pointer_type='shodow',background_color='white',
                                                        border_width=1,
                                                        textstyle_opts=opts.TextStyleOpts(color='black'),
                                                        formatter=(JsCode(tool_js))
                                                        )
                        )
        .render("./China_2019_nCovid_map.html")
)