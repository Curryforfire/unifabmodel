import numpy as np


#期数
I=2
#零件数
J=10
#机器数
K=2
#打印机版面长度
bin_height=40
#打印机版面宽度
bin_width=40

#参数设定
#sigma = np.round(np.random.uniform(1,3,size=J),2)
h = np.round(np.random.uniform(5,7,size=J),2)#每个零件平均打印耗时：6小时
tt = np.round(np.random.uniform(48,168,size=J),2)#2天-7天，按分钟计
a = np.round(np.random.uniform(5,25,size=J),2)
b = np.round(np.random.uniform(5,25,size=J),2)
s = np.round(a * b,2)
S = np.round(bin_height * bin_width,2)


#排版
Products,collect_unchosen,unchosen_copy = prodclass(a,b,tt,collect_unchosen,whdic,duetimedic)
SelectedOrder(I,J,K,h,tt,s,S)

  
      
   



