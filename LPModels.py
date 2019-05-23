#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import ParsingF as PF



def MLCP(namb):
    n=493
    m=n
    (COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()    
    nbconst=n+1
    nbvar=m+n
    rows = range(nbconst)
    columns = range(nbvar)
    
    ########################CONSTRAINTS#############################
    
    p2=[]
    constr=[]
    for i in range(n):
        p2=[]
        for j in range(nbvar-n):
            if COP1[i][j]==1:
                p2.append(1)        
            else:
                p2.append(0)
        for j in range(nbvar-n,nbvar):
            if j-m==i:
                p2.append(-1)
            else:
                p2.append(0)
        constr.append(p2)
    
    p1 = np.ones(m).tolist()
    p2 = np.zeros(n).tolist()
    p=p1+p2
    constr.append(p)
    ###########################SECOND MEMBRE###############################
    b = np.zeros(n).tolist()
    b.append(namb)
    
    
    ######################OBJECTIVE FUNCTION################################
    #dovrei utilizzare le domande dei vertici, qui posso stimarle uguali per ora
    #c = np.zeros(m).tolist()+np.ones(n).tolist()
    c=np.zeros(n).tolist()
    domtot=sum(D_U[i] for i in range(n))
    for i in range(m):
        c.append(D_U[i]/domtot)
    
    ###############################GUROBI####################################
    
    M=Model()   
    
            
    # declaration decision variables
    x = []
    for j in range(m):
        if j!=400:
            x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0, name="x%d" % j))
        else:
            x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0,ub=0, name="x%d" % j))
    for i in range(m,m+n):
        x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="y%d" %(i-m) ))
            
    # maj du modele pour integrer les nouvelles variables
    M.update()
    obj = LinExpr();
    obj =0
    for j in columns:
        obj += c[j] * x[j]
          
    # definition de l'objectif
    M.setObjective(obj,GRB.MAXIMIZE)
    # Definition des contraintes
    for i in range(0,n):
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(m+n)) >= b[i], "Constraint%d" % i)
    M.addConstr(quicksum(constr[n][j]*x[j] for j in range (m+n)) == b[n], "Constraint%d" % (i+1) )
    
    
    # Resolution
    
    M.optimize()
    
    
    k=0
    ambloc=[]
    for j in range(m):
            ambloc.append(x[k].x)
            k=k+1
    for j in range(m,n+m):
            print('y%d'%(j-m), '=', x[k].x)
            k=k+1 
    
    return(ambloc)
    
    
def LSCM():
    n=493
    m=n
    (COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()
    
    nbconst=n
    nbvar=m
    rows = range(nbconst)
    columns = range(nbvar)
    
    ########################CONSTRAINTS#############################
    
    #Les contraintes concernant le fait qu'une ville n’appartient qu’a un unique secteur et les secteurs forment une partition des n ville
    
    p2=[]
    constr=[]
    for i in range(n):
        p2=[]
        for j in range(nbvar):
            if COP1[i][j]==1:
                p2.append(1)        
            else:
                p2.append(0)
        constr.append(p2)
    
    ###########################SECOND MEMBRE###############################
    b = np.ones(n).tolist()
    b[400]=0
    
    
    ######################OBJECTIVE FUNCTION################################
    
    c = np.ones(m).tolist()
    
    ###############################GUROBI####################################
    
    M=Model()   
    
            
    # declaration decision variables
    x = []
    for j in range(m):
        if j!=400:
            x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0, name="x%d" % j))
        else:
            x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0,ub=0, name="x%d" % j))
            
    # maj du modele pour integrer les nouvelles variables
    M.update()
    obj = LinExpr();
    obj =0
    for j in columns:
        obj += c[j] * x[j]
          
    # definition de l'objectif
    M.setObjective(obj,GRB.MINIMIZE)
    
    # Definition des contraintes
    for i in range(0,n):
        M.addConstr(quicksum(constr[i][j]*x[j] for j in columns) >= b[i], "Constraint%d" % i)
    
    
    # Resolution
    
    M.optimize()
    
    
    k=0
    ambloc=[]
    for j in range(m):
            ambloc.append(x[k].x)
            k=k+1
    
    return(ambloc)


def DSM(namb,alpha):
    
    n=493
    m=n
    (COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()    
    
    nbconst=3*n+m+2
    nbvar=m+2*n
    #prima le x1, poi x2, poi y
    
    rows = range(nbconst)
    columns = range(nbvar)
    
    ########################CONSTRAINTS#############################
    
    p2=[]
    constr=[]
    
    #vincolo sulla copertura da almeno un'ambulanza in t2
    for i in range(n):
        p2=[]
        for j in range(2*n):
            p2.append(0)
        for j in range(2*n,2*n+m):
            if COP2[i][j-2*n]==1:
                p2.append(1) 
            else:
                p2.append(0)
        constr.append(p2)
    
    #vincolo per la copertura di almeno una parte di casi velocemente
    
    p2=[]
    for j in range(n):
        p2.append(D_U[j]/(sum(D_U)))
    for j in range(n,2*n+m):
        p2.append(0)
    constr.append(p2)
    
    #numero ambulanze che coprono vertici
    for i in range(n):
        p2=[]
        for j in range(2*n):
            if j-n==i or j==i:
                p2.append(-1)
            else:
                p2.append(0)
        for j in range(m):
            if COP1[i][j]==1:
                p2.append(1)        
            else:
                p2.append(0)
        constr.append(p2)
    
    #no 2 ambulanze se no 1
    for i in range(n): 
        p2=[]
        for j in range(2*n):
            if j==i:
                p2.append(-1)
            if j==i+n-1:
                p2.append(1)
            else:
                p2.append(0)
        constr.append(p2+np.zeros(m).tolist())
    
    #somma y = p     
    p1 = np.zeros(2*n).tolist()
    p2 = np.ones(m).tolist()
    p=p1+p2
    constr.append(p)
    
    # yj minore di pj
    p1=np.zeros(2*n).tolist()
    for i in range(m):
        p2=[]
        for j in range(m):
            if j==i:
                p2.append(1)
            else:
                p2.append(0)
        constr.append(p1+p2)
            
    ###########################SECOND MEMBRE###############################
    b = np.ones(n).tolist()
    #in questo sarebbe alpha*la somma dei d_i, ma ho normalizzato in questo caso, dunque=alpha
    b.append(alpha)
    b=b+np.zeros(2*n).tolist()
    b.append(namb)
    b=b+((2*np.ones(m)).tolist())
    
    
    ######################OBJECTIVE FUNCTION################################
    #dovrei utilizzare le domande dei vertici, qui posso stimarle uguali per ora
    #c = np.zeros(m).tolist()+np.ones(n).tolist()
    c=np.zeros(n).tolist()
    for i in range(m):
        c.append(D_U[i]/sum(D_U))
    c=c+np.zeros(m).tolist()
    
    ###############################GUROBI####################################
    
    M=Model()   
    
            
    # declaration decision variables
    x = []
    for j in range(n):
        x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="x1_%d" % j))
    for j in range(n):
        x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="x2_%d" % j))   
    for i in range(m):
        x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="y_%d" %i ))
            
    # maj du modele pour integrer les nouvelles variables
    M.update()
    obj = LinExpr();
    obj =0
    for j in columns:
        obj += c[j] * x[j]
          
    # definition de l'objectif
    M.setObjective(obj,GRB.MAXIMIZE)
    # Definition des contraintes
    for i in range(0,2*n+1):
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(m+2*n)) >= b[i], "Constraint%d" % i)
    for i in range(2*n+1,3*n+1):    
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(m+2*n)) <= b[i], "Constraint%d" % i)
    M.addConstr(quicksum(constr[3*n+1][j]*x[j] for j in range (m+2*n)) == b[3*n+1], "Constraint%d" % (i+1) )
    for i in range(3*n+2,3*n+m+2):    
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(m+2*n)) <= b[i], "Constraint%d" % i)
    
    # Resolution
    
    M.optimize()
    
    k=0
    for j in range(m):
            k=k+1
    for j in range(m):
            k=k+1
    
    ambloc=[]
    for j in range(m):
            ambloc.append(x[k].x)
            k=k+1
    return(ambloc)
    
def MEXCLP(namb,q):
    n=493
    m=n
    namb=29
    (COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()
                    
    
    nbconst=n+1
    nbvar=n+n*namb
    rows = range(nbconst)
    columns = range(nbvar)
    
    ########################CONSTRAINTS#############################
    
    p2=[]
    constr=[]
    for i in range(n):
        p2=[]
        for j in range(n):
            if COP1[i][j]==1:
                p2.append(1)        
            else:
                p2.append(0)
        for k in range(n,i*namb+n):
                p2.append(0)
        for k in range(i*namb+n,(i+1)*namb+n):
                p2.append(-1)
        for k in range((i+1)*namb+n,nbvar):
                p2.append(0)
    
        constr.append(p2)
                
                
        
    
    
    p1 = np.ones(m).tolist()
    constr.append(p1)
    ###########################SECOND MEMBRE###############################
    b = np.zeros(n).tolist()
    b.append(namb)
    
    
    ######################OBJECTIVE FUNCTION################################
    #dovrei utilizzare le domande dei vertici, qui posso stimarle uguali per ora
    #c = np.zeros(m).tolist()+np.ones(n).tolist()
    c=np.zeros(n).tolist()
    domtot=sum(D_U[i] for i in range(n))
    for i in range(m):
        for k in range(namb):
            c.append(D_U[i]/domtot*(1-q)*q**(k))
    
    ###############################GUROBI####################################
    
    M=Model()   
    
            
    # declaration decision variables
    x = []
    for j in range(m):
        if j!=400:
            x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0, name="x%d" % j))
        else:
            x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0,ub=0, name="x%d" % j))
    for i in range(n):
        for j in range(namb):
            x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="y%d,%d" %(i,j) ))
            
    # maj du modele pour integrer les nouvelles variables
    M.update()
    obj = LinExpr();
    obj =0
    for j in columns:
        obj += c[j] * x[j]
          
    # definition de l'objectif
    M.setObjective(obj,GRB.MAXIMIZE)
    # Definition des contraintes
    for i in range(0,n):
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(nbvar)) >= b[i], "Constraint%d" % i)
    M.addConstr(quicksum(constr[n][j]*x[j] for j in range (n)) <= b[n], "Constraint%d" % (i+1) )
    
    
    # Resolution
    
    M.optimize()
    k=0
    ambloc=[]
    
    k=0
    ambloc=[]
    for j in range(m):
            ambloc.append(x[k].x)
            k=k+1
    return(ambloc)

    
    
    

def DDSMt(namb,alpha,ambloc,tl):
    """
    start = timeit.default_timer()
    """
    n=493
    m=n
    (COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()    
    
    #nbconst=4*n+namb+1
    nbconst=4*n+namb+2
    nbvar=2*n+namb*n
    #prima le x1, poi x2, poi y
    
    rows = range(nbconst)
    columns = range(nbvar)
    """Costruire matrice spostamenti (493 righe*493colonne)
    Verificare posizionamento zone per stimare costo spostamento
    da una zona all'altra """
    """
    ambloc=np.array([1]*namb+[0]*(n-namb))
    np.random.shuffle(ambloc)
    """
    #ambpos=[i for i, x in enumerate(ambloc) if x>=1]
    #ambpos.append(next(i for i, x in enumerate(ambloc) if x>=2))
    ambpos=[]
    for i in range(n):
        if ambloc[i]>=1:
            a=ambloc[i]
            while a>0:
                ambpos.append(i)
                a=a-1
    
    print(ambpos)
    


    
    ########################CONSTRAINTS#############################
    
    p2=[]
    constr=[]
    
    #vincolo sulla copertura da almeno un'ambulanza in t2
    for i in range(n):
        p2=[]
        for j in range(2*n):
            p2.append(0)
        for j in range(2*n,2*n+m):
            if COP2[i][j-2*n]==1:
                for k in range(namb):
                    p2.append(1) 
            else:
                for k in range(namb):
                    p2.append(0)
        constr.append(p2)
    
    #vincolo per la copertura di almeno una parte di casi velocemente
    
    p2=[]
    for j in range(n):
        p2.append(D_U[j]/(sum(D_U)))
    for j in range(n,2*n+n*namb):
        p2.append(0)
    constr.append(p2)
    
    #numero ambulanze che coprono vertici
    for i in range(n):
        p2=[]
        for j in range(2*n):
            if j-n==i or j==i:
                p2.append(-1)
            else:
                p2.append(0)
        for j in range(m):
            if COP1[i][j]==1:
                for k in range(namb):
                    p2.append(1)        
            else:
                for k in range(namb):
                    p2.append(0)
        constr.append(p2)
    
    #no 2 ambulanze se no 1
    for i in range(n): 
        p2=[]
        for j in range(2*n):
            if j==i:
                p2.append(-1)
            if j==i+n-1:
                p2.append(1)
            else:
                p2.append(0)
        constr.append(p2+np.zeros(n*namb).tolist())
    
    #somma yjl = 1    
    p1 = np.zeros(2*n).tolist()
    for k in range(namb):
        p2=[]
        for j in range(nbvar-2*n):
            if (j-k)%(namb)==0:
                p2.append(1)
            else:
                p2.append(0)
        constr.append(p1+p2)
    
    # Somma yj minore di pj
    p1=np.zeros(2*n).tolist()
    for i in range(m):
        p2=[]
        for j in range(m):
            if j==i:
                for k in range(namb): 
                    p2.append(1)
            else:
                for k in range(namb):
                    p2.append(0)
        constr.append(p1+p2)
            
    ###########################SECOND MEMBRE###############################
    b = np.ones(n).tolist()
    #in questo sarebbe alpha*la somma dei d_i, ma ho normalizzato in questo caso, dunque=alpha
    b.append(alpha)
    b=b+np.zeros(2*n).tolist()
    b=b+np.ones(namb).tolist()
    b=b+((2*np.ones(m)).tolist())
    
    
    ######################OBJECTIVE FUNCTION################################
    #dovrei utilizzare le domande dei vertici, qui posso stimarle uguali per ora
    #c = np.zeros(m).tolist()+np.ones(n).tolist()
    c=np.zeros(n).tolist()
    for i in range(m):
        c.append(D_U[i]/sum(D_U))
    
    #Parte relativa a costi spostamento  (MATRICE, ma qui in teoria vettore)  
    p2=[]
    for i in range(n):
        for j in ambpos:
            if i==j:
                p2.append(0)
            else:
                p2.append(-0.1)
    c=c+p2
    ###############################GUROBI####################################
    
    M=Model()   
    M.setParam('TimeLimit', tl)
            
    # declaration decision variables
    x = []
    for j in range(n):
        x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="x1_%d" % j))
    for j in range(n):
        x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="x2_%d" % j))  
    for i in range(n):
        for j in ambpos:
            x.append(M.addVar(vtype=GRB.BINARY
                              , lb=0, name="y_%d_%d" %(i,j) ))
            
    # maj du modele pour integrer les nouvelles variables
    M.update()
    obj = LinExpr();
    obj =0
    for j in columns:
        obj += c[j] * x[j]
        

    # definition de l'objectif
    M.setObjective(obj,GRB.MAXIMIZE)
    # Definition des contraintes
    for i in range(0,2*n+1):
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(nbvar)) >= b[i], "Constraint%d" % i)
    for i in range(2*n+1,3*n+1):    
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(nbvar)) <= b[i], "Constraint%d" % i)
    for i in range(3*n+1,3*n+1+namb):
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range (nbvar)) == b[i], "Constraint%d" % i )
    for i in range(3*n+1+namb,4*n+1+namb):    
        M.addConstr(quicksum(constr[i][j]*x[j] for j in range(nbvar)) <= b[i], "Constraint%d" % i)  
    M.addConstr(quicksum(c[j]*x[j] for j in range(nbvar)) >= -0.1, "Constraint%d" % (4*n+1+namb))
    # Resolution
    
    M.optimize()
    
    if M.status == GRB.Status.OPTIMAL:
        
        print("")                
        print('Solution optimale:')
        
        k=0
        for j in range(m):
                #print('x1_%d'%(j), '=', x[k].x)
                k=k+1
        for j in range(m):
                #print('x2_%d'%(j), '=', x[k].x)
                k=k+1
        
        ambloc=np.zeros(n)
        for j in range(n):
            for h in ambpos:
                if x[k].x>=1:
                    print('y_%d_%d'%(j,h), '=', x[k].x)
                    ambloc[j]=ambloc[j]+x[k].x
                k=k+1
        ambloc=ambloc.tolist()
        
          
        print("")
        print('Objective function value :', M.objVal) 
        
        """
        stop = timeit.default_timer()
        print('Time: ', stop - start) 
        M =M.write("DDSMt.lp")
        """
        
        ### METTERE CONDIZIONE SE NO MODELLO RITORNA AMBLOC
        return(ambloc)
    
    elif M.status == GRB.Status.INFEASIBLE:
        print("No relocation")
        return 0
    return 0
