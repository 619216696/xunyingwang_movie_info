import pymysql

db = pymysql.connect(host = 'localhost',user = 'root',password = '*******',db = 'movie',charset = 'utf8')
cur = db.cursor()

class Sql:

    @classmethod
    def insert_movie(cls,movie_name,movie_director,movie_star,movie_type,movie_area,movie_language,movie_year,movie_score):
        sql = 'insert into xyw_movie_info(Name,Director,Star,Type,Area,Language,Year,Score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        cur.execute(sql,(movie_name,movie_director,movie_star,movie_type,movie_area,movie_language,movie_year,movie_score))
        db.commit()

    @classmethod
    def if_exists(cls,movie_name):
        sql = "select exists(select 1 from xyw_movie_info where Name=%s)"
        cur.execute(sql,movie_name)
        result = cur.fetchall()[0][0]
        return int(result)
