# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:19:12 2019

@author: ffede
"""

import os
from gurobipy import *
import numpy as np
import timeit
import matplotlib.pyplot as plt
import pandas as pd
import ParsingF as PF
#from oct2py import Oct2Py
#octave = Oct2Py('C:\Users\Heather\Octave-5.1.0.0\bin\octave-cli.exe')

start = timeit.default_timer()
namb=29
alpha=0.95
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

        
# variabili di decisione x1
x = []
for j in range(n):
    x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0, name="x1_%d" % j))
for j in range(n):
    x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0, name="x2_%d" % j))   
for j in range(m):
        x.append(M.addVar(vtype=GRB.BINARY
                          , lb=0, name="y%d" % j))
        
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

print("")                
print('Solution optimale:')


k=0
for j in range(m):
        print('x1_%d'%(j), '=', x[k].x)
        k=k+1
for j in range(m):
        print('x2_%d'%(j), '=', x[k].x)
        k=k+1

ambloc=[]
for j in range(m):
        #print('y_%d'%(j), '=', x[k].x)
        ambloc.append(x[k].x)
        k=k+1
     
print("")
print('Value of the objective function :', M.objVal) 

stop = timeit.default_timer()

print('Time: ', stop - start) 


##### SEZIONE X GENERARE ZONE SINGOLA-DOPPIA COPERTURA ######
filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','S_DSM'+repr(alpha)+'.txt')
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
 
filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','D_DSM'+repr(alpha)+'.txt')
f = open(filepath,'w') 
for i in range(n):
    f.write( repr(i) + ' ' + repr(Dcop[i]) + '\n' )
f.close()

filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','ambloc_DSM'+repr(alpha)+'.txt')
#if not os.path.exists(r'C:\Users\ffede\Google Drive\Reading_\Figure'):
    #os.makedirs(r'C:\Users\ffede\Google Drive\Reading_\Figure')
f = open(filepath,'w') 

for i in range(0,n):
    f.write( repr(i) + ' ' + repr(ambloc[i]) + '\n' )
f.close()

### METRICHE DI VALUTAZIONE STATICHE
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

filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','expcover_DSM1.txt')
f = open(filepath,'w') 

for i in range(0,n):
    f.write( repr(i) + ' ' + repr(ExpCov[i]) + '\n' )
f.close()

print('Percentuale singola copertura: ', Scoppercent)
print('Percentuale doppia copertura: ', Dcoppercent)


M =M.write("DSM.lp")

