#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from gurobipy import *
import numpy as np
import timeit
import matplotlib.pyplot as plt
import pandas as pd
import ParsingF as PF

start = timeit.default_timer()
n=493
m=n
namb=29
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
          
#print('\nOptimal solution:')


k=0
ambloc=[]
for j in range(m):
        #print('x%d'%j, '=', x[k].x)
        ambloc.append(x[k].x)
        k=k+1
r"""        
for j in range(m,n+m):
        print('y%d'%(j-m), '=', x[k].x)
        k=k+1
"""
#print('\nObjective function value :', M.objVal) 

k=0
amblocMCLP=[]
for j in range(m):
        amblocMCLP.append(x[k].x)
        k=k+1
h=1


##### SEZIONE X GENERARE ZONE SINGOLA-DOPPIA COPERTURA ######
filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','S_MCLP'+repr(h)+'.txt')
#if not os.path.exists(r'C:\Users\ffede\Google Drive\Reading_\Figure'):
    #os.makedirs(r'C:\Users\ffede\Google Drive\Reading_\Figure')

coptot=0
Scop=[]
for i in range(n):
    for j in range(n):
        if ambloc[j]>=1:
            if COP1[i][j]==1:
                coptot=coptot+ambloc[j]
    if coptot>=1:
        Scop.append(1)
    else:
        Scop.append(0)
    coptot=0
else:
    Scop.append(0)


    
f = open(filepath,'w') 
for i in range(n):
    f.write( repr(i) + ' ' + repr(Scop[i]) + '\n' )
f.close()


#funzione per verificare doppia copertura
coptot=0
Dcop=[]
for i in range(n):
    if Scop[i]==1:
        for j in range(n):
            if ambloc[j]>=1:
                if COP1[i][j]==1:
                    coptot=coptot+ambloc[j]
        if coptot>=2:
            Dcop.append(1)
        else:
            Dcop.append(0)
        coptot=0
    else:
        Dcop.append(0)
 
filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','D_MCLP'+repr(h)+'.txt')
f = open(filepath,'w') 
for i in range(n):
    f.write( repr(i) + ' ' + repr(Dcop[i]) + '\n' )
f.close()

filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','ambloc_MCLP'+repr(h)+'.txt')
#if not os.path.exists(r'C:\Users\ffede\Google Drive\Reading_\Figure'):
    #os.makedirs(r'C:\Users\ffede\Google Drive\Reading_\Figure')
f = open(filepath,'w') 

for i in range(0,n):
    f.write( repr(i) + ' ' + repr(ambloc[i]) + '\n' )
f.close()


stop = timeit.default_timer()

print('\nTime: ', stop - start)

Scoppercent=0
for i in range(n):
    if Scop[i]==1:
        Scoppercent=Scoppercent+D_U[i]
Scoppercent=Scoppercent/sum(D_U)
 
Dcoppercent=0       
for i in range(n):
    if Dcop[i]==1:
        Dcoppercent=Dcoppercent+D_U[i]
Dcoppercent=Dcoppercent/sum(D_U)

ExpCov=np.zeros(493)  
for i in range(n):
    if ambloc[i]==1:
        for j in range(n):
            if COP1[i][j]==1:
                ExpCov[j]=ExpCov[j]+0.6
ExpCov=ExpCov.tolist()

filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','expcover_MCLP.txt')
f = open(filepath,'w') 

for i in range(0,n):
    f.write( repr(i) + ' ' + repr(ExpCov[i]) + '\n' )
f.close()



print('Percentuale singola copertura: ', Scoppercent)
print('Percentuale doppia copertura: ', Dcoppercent)
 
M =M.write("MCLP.lp")