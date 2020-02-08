import numpy as np


#期数
I=2
#零件数
J=500
#机器数
K=2
#打印机版面长度
bin_height=60
#打印机版面宽度
bin_width=60

#参数设定
sigma = np.round(np.random.uniform(1,3,size=J),2)
h = np.round(np.random.uniform(300,420,size=J),2)#每个零件平均打印耗时：6小时
tt = np.round(np.random.uniform(2880,10080,size=J),2)#2天-7天，按分钟计
a = np.round(np.random.uniform(10,30,size=J),2)
b = np.round(np.random.uniform(10,30,size=J),2)
s = np.round(a * b,2)
S = np.round(bin_height * bin_width,2)

  
#排版
Products = prodclass(a,b,tt)
SelectedOrder(I,J,K,h,tt,s,S,sigma)

      




