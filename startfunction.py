import numpy as np
from gurobipy import *

#期数
I=3
#零件数
J=20
#机器数
K=2
#打印机版面长度
bin_height=60
#打印机版面宽度
bin_width=60
rectangles = []
for i in range(100):
    a = np.random.randint(1,60)
    b = np.random.randint(1,60)
    rectangles.append((a,b))
#参数设定
sigma = np.round(np.random.uniform(1,3,size=J),2)
h = np.round(np.random.uniform(300,420,size=J),2)#每个零件平均打印耗时：6小时
tt = np.round(np.random.uniform(2880,10080,size=J),2)#2天-7天，按分钟计
a = np.round(np.random.uniform(10,30,size=J),2)
b = np.round(np.random.uniform(10,30,size=J),2)
s = np.round(a * b,2)
S = np.round(bin_height * bin_width,2)
    

#第一步：选出150%版面工单
SelectedOrder(I,J,K,h,tt,s,S,sigma)

#第二步：100%排版
rectangles = []
for j in range(J):
    rectangles.append((a[j],b[j]))
rec_packing(rectangles,bin_width,bin_height)



