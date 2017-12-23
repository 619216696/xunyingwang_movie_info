import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from movie.items import MovieItem
from movie.mysqlpipelines.sql import Sql

class Myspider(scrapy.Spider):

    name = 'movie'
    allowed_domains = ['xunyingwang.com']

    def start_requests(self):
        yield Request('http://www.xunyingwang.com/movie',callback=self.parse)

    def parse(self,response):
        max_num = BeautifulSoup(response.text,'lxml').find('div',class_ = 'pager-bg').find_all('a')[7]['data-ci-pagination-page']
        for i in range(1,int(max_num)+1):
            url = 'http://www.xunyingwang.com/movie/?page=' + str(i)
            yield Request(url,callback=self.get_movie_url)

    def get_movie_url(self,response):
        tds = BeautifulSoup(response.text,'lxml').find('div',class_ = 'col-xs-12').find_all('h1')
        for td in tds:
            movie_url = td.find('a')['href']
            movie_name = td.find('a').get_text()
            if(Sql.if_exists(movie_name)==1):
                print('电影信息已经存在')
                continue
            yield Request(movie_url,callback=self.get_movie_info,meta={'name':movie_name})

    def get_movie_info(self,response):
        item = MovieItem()
        name_year_info = BeautifulSoup(response.text, 'lxml').find('h1').get_text()
        item['movie_name'] = response.meta['name']
        item['movie_year'] = name_year_info[-5:-1]
        tds = BeautifulSoup(response.text,'lxml').find('table',class_ = 'table table-striped table-condensed table-bordered').find('tbody').find_all('tr')
        item['movie_director'] = tds[0].find_all('td')[1].get_text()
        item['movie_star'] = tds[2].find_all('td')[1].get_text().replace('显示全部','')
        item['movie_type'] = tds[3].find_all('td')[1].get_text()
        item['movie_area'] = tds[4].find_all('td')[1].get_text()
        item['movie_language'] = tds[5].find_all('td')[1].get_text()
        item['movie_score'] = tds[-1].find_all('td')[1].get_text()
        return item


