# 使用招聘信息分析数据分析岗位的薪资、城市分布等情况

## 介绍

- 使用scrapy spider 爬取某网站全国数据分析岗位信息，MongoDB作为数据库
- 另外一网站页面由js跳转，使用splash处理js加载
- 另外 3、4网站ing……

## 代码使用

- 推荐使用docker-compose

~~~ bash
docker-compose up -d
~~~

- 非docker方式

~~~ bash
pip install -r requirements.txt
# 对于BXXX网站需使用splash
docker pull scrapinghub/splash
# mongoDB
docker pull mongo
# scrpay crawl lagou

~~~

## 2019.12.16

- flask+Vue+pyecharts可视化

## 接下来……

- 用sparkstreaming实现准实时分析