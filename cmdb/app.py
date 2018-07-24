# encoding:utf-8
import sys

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from functools import wraps  # 用于解决装饰器的bug
from flask import flash

# import users
import usersdb as users
import os
from log_analysedb import get_topn, db_insert_logs

app = Flask(__name__)

app.secret_key = os.urandom(32)  # 为session生成随机key

reload(sys)
sys.setdefaultencoding('utf-8')  # 设置命令行为utf-8


@app.route('/')
def index():
    return render_template('login.html')  # 登录跳转到login页面


@app.route('/test/')
def test():
    return render_template('user_test.html')


def login_require(func):
    @wraps(func)
    def wrapper(*args, **kwargs):  # 定义不同类型的传参
        # if not session.get('user', ''):  # 注意 '' =! None
        if not session.get('user'):  # 注意 get函数默认返回None
            return redirect('/')
        rt = func(*args, **kwargs)
        return rt

    return wrapper


# log analyze 非数据库操作
@app.route('/log/')
def log_analyze():
    topn = request.args.get('topn', '')
    topn = int(topn) if str(topn).isdigit() else 10
    rt_list = get_topn(topn)
    return render_template('logs.html', title='top10', rt_list=rt_list)


@app.route('/log/file_import/')
def logfile_import():
    return render_template('log_import.html')


@app.route('/log/data_import/', methods=['POST'])
def logdata_import():
    print request.files
    logfile = request.files.get('logfile', '')
    if logfile:
        print logfile.filename
        path = '.\\files\\ngnix.log'
        logfile.save(path)
        db_insert_logs(path)
    return redirect('/log/')


@app.route('/login/', methods=['POST'])  # post方式获取数据
def login():
    para = request.form if request.method == 'POST' else request.args
    username = para.get('username', '')
    pwd = para.get('password', '')
    print username, pwd
    _is_ok = users.validate_login(username, pwd)  # 检验用户信息是否合规
    print _is_ok
    if _is_ok:
        session['user'] = {'username': username}
        return redirect('/users/')  # 成功就跳转到users list
    else:
        return render_template('login.html', err='用户名或密码错误', username=username)  # 不成功则继续显示登录界面，并给出错误提示


# 清除缓存，实现退出功能
@app.route('/logout/')
def logout():
    print session
    session.clear()
    if not session:
        return redirect('/')


# 显示用户列表
@app.route('/users/')
@login_require
def show_users():
    users_list = users.get_users()  # 获取用户信息
    # print users_list
    print session
    return render_template('users.html', users=users_list)  # 渲染用户列表模版，显示所有用户信息


# 用户添加界面
@app.route('/user/add/', methods=['POST', 'GET'])
@login_require
def add_user():
    return render_template('user_add.html')


# 用户添加功能实现
@app.route('/user/create/', methods=['POST', 'GET'])
def create_user():
    para = request.form if request.method == 'POST' else request.args
    username = para.get('username', '')
    password = para.get('password', '')
    age = para.get('age', '')
    gender = para.get('gender', '1')
    hobby = para.getlist('hobby')
    print para
    print gender
    print hobby

    _is_ok, err = users.validate_user_create(username, password, age)  # 获取检验状态及错误信息
    print _is_ok, err
    if _is_ok:
        users.user_create(username, password, age)
        flash('添加用户成功')
        return redirect('/users/')
    # return redirect(url_for('show_users', msg='添加用户成功'))  # 不常用，了解一下
    else:
        return render_template('user_add.html', err=err, username=username, password=password, age=age)


# 用户修改界面
@app.route('/user/modify/', methods=['GET'])
def modify_user():
    para = request.form if request.method == 'POST' else request.args
    print para
    id = para.get('id', '')
    username = ''
    password = ''
    age = ''
    err = ''
    if not id:
        err = '用户信息不存在'
    else:
        _user = users.get_user(id)  # 通过get方式获取到username,从文本中获取用户信息，不要将所有信息通过get方式传递，不安全
        username = _user.get('username', '')
        password = _user.get('password', '')
        age = _user.get('age', '')

    return render_template('user_modify.html', err=err, id=id, username=username, password=password, age=age)


# 用户信息修改实现
@app.route('/user/update/', methods=['POST'])
def update():
    para = request.form if request.method == 'POST' else request.args
    id = para.get('id', '')
    username = para.get('username', '')
    password = para.get('password', '')
    age = para.get('age', '')
    print username, password, age
    _is_ok, err = users.validate_user_update(password, age)  # 获取检验状态及错误信息,这里设置不允许修改用户名
    # print _is_ok, err
    if _is_ok:
        users.user_update(id, password, age)
        flash('修改用户成功')
        return redirect('/users/')
    else:
        return render_template('user_modify.html', err=err, username=username, password=password, age=age)


# 用户删除函数，不需要界面
@app.route('/user/drop/')
def drop_user():
    para = request.form if request.method == 'POST' else request.args
    id = para.get('id', '')
    print id
    users.user_delete(id)
    flash('删除用户成功')
    return redirect('/users/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
