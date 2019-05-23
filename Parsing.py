# -*- coding: utf-8 -*-
def Parsing():
    import re
    import ParsingF as PF
    n=493
    f=open("lpcm.dat", "r")
    mat = []
    for k in range(5):
        f.readline()
    for i in range(1,n+1):
        line = f.readline()
        cleanline=line.split("\t")
        if cleanline[0]==str(i):
            i=i+1;
            mat1=[]
            cleanline=line.split("\t")
            cleanline[n]=re.sub(';\n', '',cleanline[n])
            for i in range(1,n+1):
                match = float(cleanline[i])
                mat1.append(match)
            mat.append(mat1)
    
    matv = []
    for k in range(2):
        line=f.readline()
    for i in range(1,n+1):
        line = f.readline()
        cleanline=line.split("\t")
        if cleanline[0]==str(i):
            i=i+1;
            mat1=[]
            cleanline=line.split("\t")
            cleanline[n]=re.sub(';\n', '',cleanline[n])
            for i in range(1,n+1):
                match = float(cleanline[i])
                mat1.append(match)
            matv.append(mat1)
    
    
    for k in range(4):
        f.readline()
    D=PF.Parsingvettori(n,f)
    
    for k in range(2):
        f.readline()
    K=PF.Parsingvettori(n,f)
    
    for k in range(2):
        f.readline()
    V=PF.Parsingvettori(n,f)
    
    f.close()
    return(mat,matv,D,K,V)