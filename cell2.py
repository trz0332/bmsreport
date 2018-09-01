import time
from openpyxl.utils import get_column_letter
from openpyxl.utils import column_index_from_string

    return val
t1=time.time()
for a in range(1,18279):

    b=f(a)
    #print(b)
    c=f2(b)
    #print(c)
print(time.time()-t1)
t1=time.time()
for a in range(1,18279):
    b=get_column_letter(a)
    #print(b)
    c=column_index_from_string(b)
    #print(c)
print(time.time()-t1)