# encoding:utf-8

from flask import Flask
from log_analyse import get_topn
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello reboot'


@app.route('/index')
def test():
    return 'hello reboot'


@app.route('/log/')
def log_analyze():
    logfile = 'D:\git\www\cmdb\\files\\ngnix.log'
    rt_list = get_topn(logfile=logfile)
    print rt_list
    return render_template('../last_version/logs.html', title='top10', rt_list = rt_list)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9001, debug=True)
