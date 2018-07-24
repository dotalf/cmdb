# encoding:utf-8

# kye = > (ip,url,code)
# value - > cnt
import MySQLdb
from dbutils import execute_sql, execute_bulk_commit


def db_insert_logs(logfile):
    rt_list = []
    h1 = open(logfile, 'r')
    while True:
        ctx = h1.readline()
        _log = ctx.split()
        if not ctx:
            break
        key = (_log[0], _log[6], _log[8])
        rt_list.append(key)
    h1.close()
    _sql = 'INSERT INTO logs(url,ip,code) VALUES(%s,%s,%s)'
    execute_bulk_commit(_sql, args=rt_list)


def get_topn(topn=10):
    _sql = 'select url,ip,code,count(1) from logs group by url,ip,code order by count(1) desc LIMIT %s'
    args = (topn,)
    # print _sql,args
    _rt_list, _cnt = execute_sql(_sql, args, fetch=True)
    return _rt_list


if __name__ == '__main__':
    print get_topn(10)
