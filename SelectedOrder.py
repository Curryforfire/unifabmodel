from gurobipy import *

def SelectedOrder(I,J,K,h,tt,s,S,sigma):
    #I：期数；J：零件数；K：机器数；
    
    m=Model('UnionFab_Model')
    
    #变量
    h_bar=m.addVars(I,K,lb=0,vtype=GRB.CONTINUOUS,name="h_bar")
    Y_a=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_a")
    Y_b=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_b")
    Y_bar=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_bar")
    x=m.addVars(I,J,K,vtype=GRB.BINARY,name="x")
    delta=m.addVars(I,K,vtype=GRB.BINARY,name="delta")
    
    
    
    #目标
    obj = quicksum((quicksum(sigma[j]*Y_bar[i,j,k] for j in range (J)) + (delta[i,k] * i)) for i in range (I) for k in range (K))
    m.setObjective(obj,GRB.MINIMIZE)

    #约束
    m.addConstrs(h_bar[i,k] >= h[j] * x[i,j,k] for i in range (I) for j in range (J) for k in range (K))
    m.addConstrs(((((i+1)*10)+quicksum(h_bar[t,k] for t in range (i+1)))*x[i,j,k]) == Y_a[i,j,k] for i in range (I) for j in range (J) for k in range (K))
    m.addConstrs(tt[j]*x[i,j,k] >= Y_b[i,j,k] for i in range (I) for j in range (J) for k in range (K))   
    m.addConstrs(Y_bar[i,j,k]>=Y_a[i,j,k]-Y_b[i,j,k] for i in range (I) for j in range (J) for k in range (K) ) 
    m.addConstrs(quicksum(s[j]*x[i,j,k] for j in range (J)) <= (1.5 * S) for i in range (I) for k in range (K))
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
#                Prod_KI[k][i] += collect_unchosen
                rec_packing(Prod_KI[k][i],bin_width,bin_height)
    
            
            
            
#Products = []
#for i in range(15):
#    Products.append(Product(np.random.randint(5,30),np.random.randint(5,30)))
#    print(Products[i])              
            
            
            
            