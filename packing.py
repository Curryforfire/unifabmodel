cur_width=[]
cur_width.append(0)                  
cmax_height=[]
cmax_height.append(0) 
max_height = 0#初始最大高度位0
item_selected=[[]] 
cur_layer=1
width_topright=[[]]
height_topright=[[]]
item_topright=[[]] 
t=0
i=0
layer_index=0
import numpy as np
def rec_packing(rectangles,bin_width,bin_height):
    s1=0
    s2=0
    S=bin_width*bin_height
    rec_sorted=sorted(rectangles,key=lambda s: (s[1],s[0]),reverse=True)                              
    layer_index = 0                                
    nextlayer(cur_layer,rec_sorted,cur_width,item_selected,max_height,layer_index,i=0)    
    topright(item_selected,cur_layer,rec_sorted,cmax_height,layer_index,i=0,width=0,height=0)
    for i in range(cur_layer+1):
        for j in range(len(item_selected[i])):
            s1 += item_selected[i][j][0]*item_selected[i][j][1]
    for i in range(cur_layer+1):
        try:
            for j in range(len(item_topright[i])):
                s2 += item_topright[i][j][0]*item_topright[i][j][1]
        except:
            continue
    print("\nOccupancy Rate: {:.3f}".format((s1+s2)/S))
    
def nextlayer(cur_layer,rec_sorted,cur_width,item_selected,max_height,layer_index,i=0):       #cur_layer是最高层数 而layer_index是需要遍历的每一层    
    if rec_sorted != []: 
        if max_height + rec_sorted[-1][1] <= bin_height:                     #这种情况满足的条件就是rec_sorted非空
            for r in rec_sorted[:]:
                if max_height + r[1] <= bin_height:
                    firstfit(r,rec_sorted,max_height,layer_index=i)
            cmax_height.append(0)
            cmax_height[i]=item_selected[i][0][1]                        # any problem ???
            max_height += cmax_height[i]
            print("\n{:.0f} layer packed items :".format(i+1),item_selected[i])
            if r not in item_selected:  
                i += 1
                nextlayer(cur_layer,rec_sorted,cur_width,item_selected,max_height,layer_index,i)  

def firstfit(r,rec_sorted,max_height,layer_index): 
    cur_width.append(0)
    if cur_width[layer_index] + r[0] <= bin_width:    
        cur_width[layer_index] += r[0]
        item_selected.append([])
        item_selected[layer_index].append(r)
        rec_sorted.remove(r)
        
def topright(item_selected,cur_layer,rec_sorted,cmax_height,layer_index=0,i=0,width=0,height=0):
    while item_selected[i] != []:
        item_selected[i].reverse()
        for r in item_selected[i]:     
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
    toprightlayer(cur_layer,rec_sorted,cmax_height,i,t,layer_index)
    
def toprightlayer(cur_layer,rec_sorted,cmax_height,i,t,layer_index):
    i=0
    if rec_sorted != []:
        while layer_index < len(cmax_height):
            for i in range(len(width_topright[layer_index])):
                for r in rec_sorted: 
                    if i + 1 <= len(width_topright[layer_index]): 
                        if t + r[0] <= width_topright[layer_index][i] and r[1] + height_topright[layer_index][i] <= cmax_height[layer_index]:                              
                            item_topright[layer_index].append(r) 
                            t += r[0]
                            rec_sorted.remove(r)                           
            item_topright.append([])
            if item_topright[layer_index] != []:
                print("\n{:.0f} layer corner packed items :".format(layer_index+1),item_topright[layer_index])
            i=0
            t=0
            layer_index += 1
bin_height=60
#打印机版面宽度
bin_width=60
rectangles = []
for i in range(10):
    a = np.random.randint(5,30)
    b = np.random.randint(5,30)
    rectangles.append((a,b))

rec_packing(rectangles,bin_width,bin_height)            