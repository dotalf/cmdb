# encoding:utf-8

# kye = > (ip,url,code)
# value - > cnt


def get_topn(logfile, topn=10):
    access_cnt = {}

    h1 = open(logfile, 'r')
    while True:
        ctx = h1.readline()
        # print ctx
        _log = ctx.split()
        if not ctx:
            break
        key = (_log[0], _log[6], _log[8])
        access_cnt[key] = access_cnt.get(key, 0) + 1
    h1.close()

    def sort_array(array):
        for i in range(0, len(array) - 1):
            for j in range(0, len(array) - 1 - i):
                if array[j][1] > array[j + 1][1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    return sort_array(access_cnt.items())[-1:-topn - 1:-1]


if __name__ == '__main__':
    print get_topn('D:\git\www\cmdb\\files\\ngnix.log' ,topn=10)
