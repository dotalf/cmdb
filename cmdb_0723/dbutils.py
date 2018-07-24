# encoding:utf-8

# 这里定义了对数据库操作的函数
import get_conf
import MySQLdb


def execute_fetch_sql(sql, args=(), fetch=True):
    return execute_sql(sql, args, fetch)


def execute_commit_sql(sql, args=(), fetch=False):
    return execute_sql(sql, args, fetch)


# 对上面两个函数进一步融合
def execute_sql(sql, args=(), fetch=True):
    _conn = None
    _cur = None
    _cnt = None
    _rt_list = []
    try:
        _conn = MySQLdb.connect(
            host=get_conf.MYSQL_HOST, port=get_conf.MYSQL_PORT,
            user=get_conf.MYSQL_USER, passwd=get_conf.MYSQL_PASSWD, db=get_conf.MYSQL_DB,
            charset=get_conf.MYSQL_CHARSET)
        _cur = _conn.cursor()
        _cnt = _cur.execute(sql, args)
        if fetch:
            _rt_list = _cur.fetchall()
        else:
            _conn.commit()
    except BaseException as e:
        print e
    finally:  # 打开数据库及游标，才有关闭操作
        if _cur:
            _cur.close()
        if _conn:
            _conn.close()
    return _rt_list, _cnt


# 优化commit sql,一次打开，多次执行，否则每次执行一条sql都要打开及关闭游标
# 快N倍。。。
def execute_bulk_commit(sql, args=[]):
    _conn = None
    _cur = None
    _cnt = 0
    _rt_list = []
    try:
        _conn = MySQLdb.connect(
            host=get_conf.MYSQL_HOST, port=get_conf.MYSQL_PORT,
            user=get_conf.MYSQL_USER, passwd=get_conf.MYSQL_PASSWD, db=get_conf.MYSQL_DB,
            charset=get_conf.MYSQL_CHARSET)
        _cur = _conn.cursor()
        for arg in args:
            _cnt += _cur.execute(sql, arg)
        _conn.commit()
    except BaseException as e:
        print e
    finally:  # 打开数据库及游标，才有关闭操作
        if _cur:
            _cur.close()
        if _conn:
            _conn.close()
    return _cnt
