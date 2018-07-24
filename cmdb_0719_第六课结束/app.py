# encoding:utf-8

from flask import Flask
from log_analyse import get_topn
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/index')
def test():
    return 'hello reboot'


@app.route('/log/')
def log_analyze():
    logfile = 'D:\git\www\cmdb\\files\\ngnix.log'
    topn = request.args['topn']
    topn = 10 if not topn else int(topn)
    rt_list = get_topn(logfile=logfile, topn=topn)
    return render_template('../cmdb/cmdb/last_version/logs.html', title='top10', rt_list=rt_list)


@app.route('/login/', methods=['POST'])
def login():
    para = request.form if request.method == 'POST' else request.args
    print para.get('username', '')
    print request.form.get('password', '')
    return render_template('')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
