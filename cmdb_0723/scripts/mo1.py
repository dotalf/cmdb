#encoding:utf-8
import  time
import tuple_sort
from tuple_sort import cmp
my_list = [1, 4, 5, 8]

t1 = time.time()
print t1
print tuple_sort.sort_array(my_list,lambda x :x, tuple_sort.cmp)
print tuple_sort.sort_array(my_list,lambda x :x, cmp)

t2 =time.time() - t1
print t2
