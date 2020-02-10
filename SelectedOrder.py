from gurobipy import *

def SelectedOrder(I,J,K,h,tt,s,S):
    #I：期数；J：零件数；K：机器数；
    
    m=Model('UnionFab_Model')
    
    num_unchosen=0
    num_unchosen,tt1,s1 = parameter(collect_unchosen,whdic,duetimedic)
    J += num_unchosen 
       
    #变量
    h_bar=m.addVars(I,K,lb=0,vtype=GRB.CONTINUOUS,name="h_bar")
    Y_a=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_a")
    Y_b=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_b")
    Y_bar=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_bar")
#    x=m.addVars(I,J,K,vtype=GRB.BINARY,name="x")
    delta=m.addVars(I,K,vtype=GRB.BINARY,name="delta")
    
    x= addvar_x(m,I,J,K)   
    
    
    #目标
#    obj = quicksum((quicksum(sigma[j]*Y_bar[i,j,k] for j in range (J)) + (delta[i,k] * i)) for i in range (I) for k in range (K))  #之前出问题是因为sigma没有更新
    obj = quicksum((quicksum(Y_bar[i,j,k] for j in range (J)) + (delta[i,k] * i)) for i in range (I) for k in range (K))    #所以暂且把sigma扰动项去掉
    m.setObjective(obj,GRB.MINIMIZE)

    #约束
    h = np.round(np.random.uniform(5,7,size=J),2)
    m.addConstrs(h_bar[i,k] >= h[j] * x[i,j,k] for i in range (I) for j in range (J) for k in range (K))
    m.addConstrs(((((i+1)*10)+quicksum(h_bar[t,k] for t in range (i+1)))*x[i,j,k]) == Y_a[i,j,k] for i in range (I) for j in range (J) for k in range (K))
    
#    m.addConstrs(tt[j]*x[i,j,k] >= Y_b[i,j,k] for i in range (I) for j in range (J) for k in range (K))   
    addcon_tt(m,I,J,K,x,Y_b,tt,tt1)
    
    m.addConstrs(Y_bar[i,j,k]>=Y_a[i,j,k]-Y_b[i,j,k] for i in range (I) for j in range (J) for k in range (K) ) 
    
#    m.addConstrs(quicksum(s[j]*x[i,j,k] for j in range (J)) <= (1.5 * S) for i in range (I) for k in range (K))
    addcon_size(m,I,J,K,x,s,s1,S)
    
    m.addConstrs(quicksum(x[i,j,k] for i in range (I) for k in range (K)) == 1 for j in range (J))    
    m.addConstrs(quicksum(x[i,j,k] for j in range (J)) <= 10000000000000*delta[i,k] for i in range (I) for k in range (K))
    
    
    #求解
    m.Params.MIPGap = 0.5
    m.optimize()
    #m.status==gurobipy.GRB.Status.OPTIMAL
    m.printAttr('x')
    print('optimal value: %.2f'%obj.getValue())
    #for var in m.getVars():
        #print(f"{var.varName}: {round(var.x)}") 
    
    Prod_KI=[]    
    for k in range(K):
        Prod_KI.append([])
        for i in range(I):
            Prod_KI[k].append([])
            for j in range(J):
                if x[i,j,k].x == 1:
                    Prod_KI[k][i].append(Products[j])
    
    for k in range(K):
        for i in range(I):
            if Prod_KI[k][i] != []:
                print('\n machine {:.0f} at period {:.0f} :'.format(k+1,i+1))
                rec_packing(Prod_KI[k][i],bin_width,bin_height)


"""将添加约束和添加变量写成函数形式
"""     
def parameter(collect_unchosen,whdic,duetimedic): 
    """以列表形式返回每次未选中零件的尺寸、截止时间信息
    """
    num = len(collect_unchosen)
    tt_due = []
    s_size = []
    if num != 0:
        for i in range(num):
            m = collect_unchosen[i] 
            tt_due.append(duetimedic[m])
            s_size.append(whdic[m][0]*whdic[m][1])
    return (num,tt_due,s_size)

#添加变量     
def addvar_x(m,I,J,K):
    var = m.addVars(I,J,K,vtype=GRB.BINARY,name="x")
    return var            
            
#添加截止时间约束          
def addcon_tt(m,I,J,K,x,Y_b,tt,tt1):  
    tt=list(tt)
    tt += tt1    
    m.addConstrs(tt[j]*x[i,j,k] >= Y_b[i,j,k] for j in range (J) for i in range (I) for k in range (K))         

#添加底面积约束             
def addcon_size(m,I,J,K,x,s,s1,S):
    s=list(s)
    s += s1
    m.addConstrs(quicksum(s[j]*x[i,j,k] for j in range (J)) <= (1.5 * S) for i in range (I) for k in range (K))         
            
            