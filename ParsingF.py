import re

def Parsingvettori(n,f):
    Prov=[]
    for i in range(1,n+1):
        line = f.readline()
        cleanline=line.split("\t")
        if cleanline[0]==str(i):
            i=i+1;
            cleanline=line.split("\t")
            cleanline[1]=re.sub(';\n', '',cleanline[1])
            match = float(cleanline[1])
            Prov.append(match)
    return(Prov)
    
def Parsing():
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
    
    #D=domande urgenti
    for k in range(4):
        f.readline()
    D=Parsingvettori(n,f)
    
    #K=numero missioni
    for k in range(2):
        f.readline()
    K=Parsingvettori(n,f)
    
    #V=domande non urgenti
    for k in range(2):
        f.readline()
    V=Parsingvettori(n,f)
    
    f.close()
    return(mat,matv,D,K,V)