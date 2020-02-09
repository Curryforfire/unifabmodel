import numpy as np

class Product(object):
    tag = 1 #class variable,tag used to give unique id to each new product instance
    def __init__(self, width, height, duetime=None):
        self.width = width 
        self.height = height
        self.duetime = duetime
        self.rid = Product.tag
        Product.tag += 1
    def get_rid(self):
        return str(self.rid).zfill(3)  #pad the beginging with zeros, 001 not 1
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_duetime(self):
        return self.duetime        
    def __str__(self):
        return str(self.rid).zfill(3) + ': <' + str(self.width)\
                 + ', ' + str(self.height) + '>' + ' duetime:' \
                 + str(self.duetime)


"""等每一次计算完成后，将未选中的挑出重新进行计算，
然后把下式清空。感觉类的作用没有完全体现出来……
"""
collect_unchosen = []    
whdic = {}
duetimedic = {}


def prodclass(a,b,tt,collect_unchosen):
    """对生成的全体零件定义为符合零件类class的形式
    """  
    Products = []      #每次点击接着之前生成的列表，若要求默认置为空，则在函参中添加此行
    for j in range(J):        
        Products.append(Product(a[j],b[j],tt[j]))
        print(Products[j]) 
    for j in range(len(collect_unchosen)):
        m = collect_unchosen[j]
        Products.append(Product(whdic[m][0],whdic[m][1],duetimedic[m]))
        print(Products[j])
    return Products

def dic_all(Products,duetimedic,dicforall={}):
    """对全体零件集合以编码作key，（width和height）
    作为value
    """
    for i in range(len(Products)):
        dicforall[Products[i].get_rid()]=(Products[i].get_width(),Products[i].get_height())
        duetimedic[Products[i].get_rid()]=Products[i].get_duetime()
    return (dicforall,duetimedic) 

def pick(Prod_KI,dictionary={}):
    """对每一版零件单独定义字典，以本身编号作为key，
    （width和height）作为value
    """
    for i in range(len(Prod_KI)):
        dictionary[Prod_KI[i].get_rid()]=(Prod_KI[i].get_width(),Prod_KI[i].get_height())  
#    if collect_unchosen != []: 
#        for i in range(len(collect_unchosen)):
#            key = str(collect_unchosen[i])
#            dictionary[key]=dicforall[key]
    return dictionary

def unchosen(collect_unchosen,rec_unchosen,whdic,rec_dict,duedic):
    """未被选择的零件集合，字典unchosendict通过零件
    编号访问width和height，字典duetimedic通过上述key
    访问duetime    
    """    
    for i in range(len(rec_dict)):
        rec_unchosen.append(rec_dict[i][0]) 
        whdic[rec_dict[i][0]]=rec_dict[i][1]
        duetimedic[rec_dict[i][0]]=duedic[rec_dict[i][0]]
    if rec_unchosen != []:
        print("\nUnchosen items : ",rec_unchosen)   
    collect_unchosen += rec_unchosen 
    if collect_unchosen != []:
        print('so far unchosen products : ',collect_unchosen)
    return collect_unchosen 
 
def printunchosen(collect_unchosen,whdic,duetimedic):
    """输出所有未被选中的零件编号，width,height和duetime
    """
    n = len(collect_unchosen)
    for i in range(n):
        print(collect_unchosen[i],whdic[collect_unchosen[i]],duetimedic[collect_unchosen[i]])
    return n
    
def rec_packing(Prod_KI, bin_width, bin_height):
    """主函数，调用nextlayer和topright两个函数
    分别解决左下方开始和阶梯型右上角基于高度递减
    的装箱。width即水平延伸为宽度，height是二维
    平面的纵向延伸为高度。并通过分别累加s1，s2并
    对两阶段求和计算总的底面利用率。
    """ 
    cur_width=[]
    cur_width.append(0)                  
    cmax_height=[]
    cmax_height.append(0) 
    max_height = 0 
    item_existed=[[]]   
    item_selected=[[]] 
    cur_layer=1
    width_topright=[[]]  
    height_topright=[[]]
    item_topright=[[]] 
    index_topright=[[]]
    rec_dict=[]
    rec_unchosen=[]
    
    t=0
    i=0
    layer_index=0
    s1=0
    s2=0  
    S=bin_width*bin_height
    
    (dicforall,duedic) = dic_all(Products,duetimedic,dicforall={})  
    mydict = pick(Prod_KI,dictionary={}) 
    
    rec_dict = sorted(mydict.items(),key=lambda s: (s[1][1],s[1][0]), reverse=True)  
    """对零件集合组成的字典重新排序（height递减）
    但不改变对应key的值,排序后是list中套元组，元
    组中是key和对应的value
    """      
#两种装箱方式的函数                                         
    nextlayer(cmax_height,item_existed,rec_dict,Products,cur_layer,cur_width,item_selected,max_height,layer_index,i=0)    
    topright(index_topright,item_topright,t,height_topright,width_topright,rec_dict,Products,item_selected,item_existed,cur_layer,cmax_height,layer_index,i=0,width=0,height=0)
#计算两种方式和的总利用率   
    for i in range(cur_layer+1):
        for j in range(len(item_existed[i])):
            s1 += item_existed[i][j][0]*item_existed[i][j][1]
    for i in range(cur_layer+1):
        try:
            for j in range(len(item_topright[i])):
                s2 += item_topright[i][j][0]*item_topright[i][j][1]
        except:
            continue
    print("\nOccupancy Rate: {:.3f}".format((s1+s2)/S))
#输出未被打印的零件集合  
    unchosen(collect_unchosen,rec_unchosen,whdic,rec_dict,duedic)
    
    
def nextlayer(cmax_height,item_existed,rec_dict,Products,cur_layer,cur_width,item_selected,max_height,layer_index,i=0):       #cur_layer是最高层数 而layer_index是需要遍历的每一层    
    """从第一层开始，如果第i层横向有空间可装,
    则调用firsrfit进行装箱，否则判断i+1层
    """ 
    if rec_dict != []: 
        if max_height + rec_dict[-1][1][1] <= bin_height:   #这种情况满足的条件就是rec_dict非空
            for r in rec_dict[:]:              #[:]
                if max_height + r[1][1] <= bin_height:
                    firstfit(item_existed,item_selected,cur_width,rec_dict,Products,r,max_height,layer_index=i)
            cmax_height.append(0)
            cmax_height[i]=item_existed[i][0][1]
            max_height += cmax_height[i]
            print("\n{:.0f} layer packed items :".format(i+1),item_selected[i])
            if r not in item_selected:  
                i += 1
                nextlayer(cmax_height,item_existed,rec_dict,Products,cur_layer,cur_width,item_selected,max_height,layer_index,i)  
        
def firstfit(item_existed,item_selected,cur_width,rec_dict,Products,r,max_height,layer_index): 
    cur_width.append(0)
    if cur_width[layer_index] + r[1][0] <= bin_width:    
        cur_width[layer_index] += r[1][0]
        item_selected.append([])
        item_selected[layer_index].append(r[0])
        item_existed.append([])
        item_existed[layer_index].append(r[1])
        rec_dict.remove(r)
        return rec_dict 
        
def topright(index_topright,item_topright,t,height_topright,width_topright,rec_dict,Products,item_selected,item_existed,cur_layer,cmax_height,layer_index=0,i=0,width=0,height=0):
    """在第一阶段装箱结束后，会生成多层版面，每一层均为阶梯型，
    记录这些阶梯型的参数，供第二阶段倒阶梯型利用
    """
    while item_existed[i] != []:
        item_existed[i].reverse()
        for r in item_existed[i]:     
            width += r[0]
            width_topright[i].append(width)
            height_topright[i].append(r[1])
        width_topright[i].pop()
        height_topright[i].pop()
        width_topright.append([])   
        height_topright.append([])
        width = 0
        i += 1
    width_topright.pop()
    height_topright.pop()
    cmax_height.pop()
    toprightlayer(index_topright,item_topright,height_topright,width_topright,rec_dict,Products,cur_layer,cmax_height,i,t,layer_index)
    return rec_dict
    
def toprightlayer(index_topright,item_topright,height_topright,width_topright,rec_dict,Products,cur_layer,cmax_height,i,t,layer_index):  
    i=0
    if rec_dict != []:
        while layer_index < len(cmax_height):
            for i in range(len(width_topright[layer_index])):
                for r in rec_dict: 
                    if i + 1 <= len(width_topright[layer_index]): 
                        if t + r[1][0] <= width_topright[layer_index][i] and r[1][1] + height_topright[layer_index][i] <= cmax_height[layer_index]:                              
                            item_topright[layer_index].append(r[1])
                            index_topright[layer_index].append(r[0])
                            t += r[1][0]
                            rec_dict.remove(r)                           
            item_topright.append([])
            index_topright.append([])
            if index_topright[layer_index] != []:
                print("\n{:.0f} layer corner packed items :".format(layer_index+1),index_topright[layer_index])
            i=0
            t=0
            layer_index += 1

#Products = []
#for i in range(15):
#    Products.append(Product(np.random.randint(5,30),np.random.randint(5,30)))
#    print(Products[i])  
#bin_height=60  
#bin_width=60
#Products = [Product(1,1),Product(3,3),Product(1,1),Product(1,1),Product(1,1),Product(1,1),Product(1,1)]
#for i in range(len(Products)):
#    print(Products[i])
#rec_packing(Products, bin_width, bin_height)            