# encoding:utf-8

# list[(1,4), (5,1), (2,3)],根据每个元组的中的较大值进行排序
# 期待结果 [(2,3), (1,4), (5.1)]
# 要求用sorted和lambda完成
# 级别1： 用Lambda和max
# 级别2：用lambda不用max
# 提示： True * 4 == 4 False *2 == 0


list1 = [(1, 4), (5, 1), (2, 3)]

# method 1
def sort_array(array):
    for i in range(0, len(array)-1):
            for j in range(0,len(array)-1-i):
                if max(array[j]) > max(array[j+1]):
                        array[j],array[j+1] = array[j+1], array[j]
    return array

# print sort_array(list1)

# method 2
def sort_array(array,getmax):
    for i in range(0, len(array)-1):
            for j in range(0,len(array)-1-i):
                if getmax(array[j]) > getmax(array[j+1]):
                        array[j],array[j+1] = array[j+1], array[j]
    return array
# print sort_array(list1,lambda x : max(x))



# method 3
list1 = [(1, 4), (5, 1), (2, 3)]
list2  = [{'name' : 'lf11'}, {'name' : 'lf1'}, {'name' : 'lf3'} ]
def cmp(x, y):
    if x > y:
        return True
    else:
        return False

def sort_array(array,getmax,cpm):
    array = array[:]
    for i in range(0, len(array)-1):
            for j in range(0,len(array)-1-i):
                if cpm(getmax(array[j]), getmax(array[j+1])):
                        array[j],array[j+1] = array[j+1], array[j]
    return array




list2  = [{'name' : 'if11'}, {'name' : 'of1'}, {'name' : 'lf3'} ]
list2.sort(key=lambda x : x.get('nname'))
print __name__
if __name__ == '__main__':
    print sort_array(list1,lambda x : max(x),cmp)
    print sort_array(list2,lambda x : x['name'],cmp)
    print list2
