# -*- coding: utf-8 -*-
# @Time    : 2018/10/6 13:19
# @Author  : AllenOris
# @Email   : lighthouse0@163.com
# @File    : data_generator.py
# @Software: PyCharm

"""
数据测试
T<=15
2<=n<=1e5
0<=x,y<=1e9
"""
import random

with open("test.in", "w") as w:
    def write_next(*a):
        for ele in a:
            w.write(str(ele) + ' ')
        w.write('\n')


    TT = 15
    write_next(TT)
    for T in range(1, TT + 1):
        if T < 5:
            n = random.randint(2, 21)
            r = 1000
        elif T < 10:
            n = random.randint(10, 1e4)
            r = 1000
        else:
            n = random.randint(1e4, 1e5)
            r = 1e9
        write_next(n)
        for i in range(n):
            a, b = random.randint(0, r), random.randint(0, r)
            write_next(a, b)
