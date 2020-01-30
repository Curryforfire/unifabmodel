def SelectedOrder(I,J,K,h,tt,s,S,sigma):
    #I：期数；J：零件数；K：机器数；
    
    m=Model('UnionFab_Model')
    #变量
    h_bar=m.addVars(I,K,lb=0,vtype=GRB.CONTINUOUS,name="h_bar")
    Y_a=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_a")
    Y_b=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_b")
    Y_bar=m.addVars(I,J,K,lb=0,vtype=GRB.CONTINUOUS,name="Y_bar")
    x_var=m.addVars(I,J,K,vtype=GRB.BINARY,name="x_var")
    delta=m.addVars(I,K,vtype=GRB.BINARY,name="delta")
        
    #目标
    obj = quicksum((quicksum(sigma[j]*Y_bar[i,j,k] for j in range (J)) + (delta[i,k] * i)) for i in range (I) for k in range (K))
    m.setObjective(obj,GRB.MINIMIZE)

    #约束
    m.addConstrs(h_bar[i,k] >= h[j] * x_var[i,j,k] for i in range (I) for j in range (J) for k in range (K))
    m.addConstrs(((((i+1)*10)+quicksum(h_bar[t,k] for t in range (i+1)))*x_var[i,j,k]) == Y_a[i,j,k] for i in range (I) for j in range (J) for k in range (K))
    m.addConstrs(tt[j]*x_var[i,j,k] >= Y_b[i,j,k] for i in range (I) for j in range (J) for k in range (K))   
    m.addConstrs(Y_bar[i,j,k]>=Y_a[i,j,k]-Y_b[i,j,k] for i in range (I) for j in range (J) for k in range (K) ) 
    m.addConstrs(quicksum(s[j]*x_var[i,j,k] for j in range (J)) <= (1.5 * S) for i in range (I) for k in range (K))
    m.addConstrs(quicksum(x_var[i,j,k] for i in range (I) for k in range (K)) == 1 for j in range (J))    
    m.addConstrs(quicksum(x_var[i,j,k] for j in range (J)) <= 10000000000000*delta[i,k] for i in range (I) for k in range (K))
        
    #求解
    m.Params.MIPGap = 0.1
    m.optimize()
    #m.status==gurobipy.GRB.Status.OPTIMAL
    print('optimal value: %.2f'%obj.getValue())
    m.printAttr('x')
  #  fixed = m.fixed()
  
  
  
    
  
  
"""  
    vars = m.getVars()      #vars[-1]检索到的就是最后一个变量 而不考虑是不是为1
    x0 = vars[-1]           #Retrieve a list of all variables in the model. 
    print(vars[0].varName, vars[0].x)
    print(x0)
    
"""  
  
  
  
  
  
"""
    for k in range(K):
        for i in range(I):
            for j in range(J):
                u[i,j,k] = x_var[i,j,k].get()    
    print('k=1',u[i,j,k])
        
    #for var in m.getVars():
        #print(f"{var.varName}: {round(var.x)}")
"""

    