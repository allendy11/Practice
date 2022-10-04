'''
Created on Oct 4, 2022

@author: root
'''

import timeit

def add(x,y):
    return x+y
def check_time(a,b):
    add(a,b)
def test():
    a=1
    b=2
    c=check_time(a,b)
    print(c)
if __name__ == '__main__':
    a=1
    b=2
    c='1'
    d='2'
    # ss = timeit.timeit(check_time(c,d))
    # print(ss)
    # s = timeit.timeit('check_time(a, b)', 'from __main__ import check_time, a, b')
    # print(s)
    
    timeit.timeit('test()', 'from __main__ import test')