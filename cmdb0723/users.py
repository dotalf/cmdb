# encoding:utf-8

import json
import get_conf

# file = '.\\files\users.json'
file = get_conf.USERS_FILES


# 获取所有用户信息
def get_users():
    try:
        h1 = open(file, 'r')
        ctx = h1.read()
        h1.close()
        # print ctx,type(ctx)
        return json.loads(ctx)
    except BaseException as e:
        print e
        return []


# 获取单个用户信息
def get_user(username):
    _users = get_users()
    for _user in _users:
        if _user['username'] == username:
            return _users, _user


# 用户保存函数
def user_save(users):
    _users = json.dumps(users)
    h1 = open(file, 'w')
    h1.write(_users)
    h1.close()


# 校验登录用户名密码
def validate_login(username, pwd):
    users = get_users()
    for user in users:
        if username == user.get('username') and pwd == user.get('password'):
            return True, ''
    return False, u'username or password is error'


# 校验用户添加
def validate_user_create(username, pwd, age):
    users = get_users()

    # 用户名检验
    if not username:
        return False, u'用户名不能为空'
    for user in users:
        if user.get('username') == username:
            return False, u'用户名己存在'
    # 密码检验
    if not pwd:
        return False, u'密码不能为空'
    if len(pwd) < 6:
        return False, u'密码长度小于6位'

    # 年龄检验
    if not age:
        return False, u'年龄不能为空'
    # type(age) 为 unicode，最好转换为str
    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False, u'请输入0~100之间的数字'

    return True, u''


# 用户添加函数
def user_create(username, pwd, age):
    _users = get_users()
    _user = {'username': username, 'password': pwd, "age": age}
    _users.append(_user)
    # ctx = json.dumps(_users)
    # print ctx
    user_save(_users)


# 校验用户信息修改
def validate_user_update(pwd, age):
    # 密码检验
    if not pwd:
        return False, u'密码不能为空'
    if len(pwd) < 6:
        return False, u'密码长度小于6位'

    # 年龄检验
    if not age:
        return False, u'年龄不能为空'
    # type(age) 为 unicode，最好转换为str
    if not str(age).isdigit() or int(age) <= 0 or int(age) > 100:
        return False, u'请输入0~100之间的数字'

    return True, u'修改成功'


# 用户修改函数
# 判断即保存，减少判断
# 这是什么能这样修改，理解传值和传址的区别
def user_update(username, pwd, age):
    _users, _user = get_user(username)
    _user['password'] = pwd
    _user['age'] = age
    print _users
    user_save(_users)


# def user_update(username, pwd, age):
#     _users = get_users()
#     print _users
#     for _user in _users:
#         if _user['username'] == username:
#             _user['password'] = pwd
#             _user['age'] = age
#             user_save(_users)
#             break


# 用户删除函数
# 这里用get_user函数简化

def user_delete(username):
    _users, _user = get_user(username)
    _users.remove(_user)
    user_save(_users)


# def user_delete(username):
#     _users = get_users()
#     for _user in _users:
#         if _user['username'] == username:
#             _users.remove(_user)
#             print _users
#             user_save(_users)
#             break


if __name__ == '__main__':
    print user_delete('lf6')
