# -*- coding: utf-8 -*-
"""

@author: ffede
"""

import os
from gurobipy import *
import numpy as np
import timeit
import matplotlib.pyplot as plt
import pandas as pd
import ParsingF as PF

start = timeit.default_timer()
namb=29
alpha=0.95
filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','ambloc_DSM'+repr(alpha)+'.txt')
data = pd.read_csv(filepath, sep=" ", header = None)
ambloc=list(data[1])
amblocnew=0

n=493
m=n
(COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()    

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
np.random.seed(10234)
np.random.shuffle(ambloc)
"""


ambpos=[i for i, x in enumerate(ambloc) if x == 1]

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
    v=p1+p2
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
#M.setParam('TimeLimit', 0)
        
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
M.addConstr(quicksum(c[j]*x[j] for j in range(nbvar)) >= 0, "Constraint%d" % (4*n+1+namb))
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
    for j in range(m):
        for h in ambpos:
            if x[k].x>=1:
                print('y_%d_%d'%(j,h), '=', x[k].x)
                ambloc[j]=x[k].x
            k=k+1
    
    
    
       
    print("")
    print('Objective function value :', M.objVal) 
    
    stop = timeit.default_timer()
    
    print('Time: ', stop - start) 
    M =M.write("DDSMt.lp")

elif M.status == GRB.Status.INFEASIBLE:
     print("KAKAKAK")
    



