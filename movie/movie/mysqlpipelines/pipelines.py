from .sql import Sql
from movie.items import MovieItem

class Moviepipeline(object):

    def process_item(self,item,spider):
        movie_name = item['movie_name']
        movie_director = item['movie_director']
        movie_star = item['movie_star']
        movie_type = item['movie_type']
        movie_area = item['movie_area']
        movie_language = item['movie_language']
        movie_year = item['movie_year']
        movie_score = item['movie_score']
        Sql.insert_movie(movie_name,movie_director,movie_star,movie_type,movie_area,movie_language,movie_year,movie_score)
        print('开始抓取电影信息')