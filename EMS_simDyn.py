# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 22:11:02 2019

@author: ffede
......"""


import simpy
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ParsingF as PF
import LPModels as LPM
import os



(COP1,COP2,D_U,NMIS,D_NU)=PF.Parsing()
c=49
seed=9
modello="DDSMt"
#seed=random.randint(0,10000)
"""
random.seed(a=seed, version=2)
np.random.seed(seed=seed)
del(seed)
"""

### AGGIORNARE ANCHE AMBLOC?
####CAMBIARE MODELLI PER PASSARE IL VETTORE DELLE AMBULANZE

class Ambulance:
    
    
    def __init__(self,id):
        self.availability = 1
        self.id=id
        self.position=id
        self.time_in=0
        self.stasis=0
    
    #l'ambulanza va in missione, viene dunque resa indisponibile
    def dislocation(self,env,e):
        self.availability=0
        self.stasis=e.duration
       # print("Stasis",self.stasis)
        Global_vars.namb=Global_vars.namb-1
        Global_vars.ambloc[self.position]=Global_vars.ambloc[self.position]-1
        self.time_in=env.now
    
    #funzione chiamata per riattivare le ambulanze che hanno finito la missione
    def tryunfreeze (self,env):
        if (abs(env.now-self.time_in)>self.stasis):
            #print("unfreezed",self.id)
            self.availability=1
            Global_vars.namb=Global_vars.namb+1
            Global_vars.ambloc[self.position]=Global_vars.ambloc[self.position]+1

"""
    def displayCount(self):
        print ("# Ambulances: "), self.ambcount
     
    def displayAmb(self):
        print ("Id : "), self.id,  (", Availability: "), self.availability
"""   

#functions to manage emergencies allocating the right ambulance
"""Idea alla base: In base alla priorità l'allocator chiama un manager, il quale
controlla se l'ambulanza passata riesce ad arrivare in tempo a coprire l'emergenza.
Se riesce, restituisce 1, altrimenti restituisce 0 e si passa a controllare l'ambulanza
successiva. Se riesce, inserisce nell'evento anche il tempo di soluzione (1,2,3)    
e lo contrassegna come solved.
"""
def AmbulanceManager1(A,env,e):
    success=0
    #print("Manager 1")
    if A.availability==1:
        #print(A.id,e.zone)
        if COP1[A.id][e.zone]==1:
            success=1
            A.dislocation(env,e)
            #print("dislocation of:", A.id)
            e.solution(1)
            return(success)
    return(success)

def AmbulanceManager2(A,env,e):
    success=0
    #print("Manager 2")
    if A.availability==1:
        #print(A.id,e.zone)
        if COP2[A.id][e.zone]==1:
            success=1
            A.dislocation(env,e)
            #print("dislocation of:", A.id)
            if COP1[A.id][e.zone]==1:
                e.solution(1)
            else:
                e.solution(2)
            return(success)
    return(success)
    
def AmbulanceManager3(A,env,e):
    success=0
    #print("Manager 3")
    if A.availability==1:
        success=1
        A.dislocation(env,e)
        #print("dislocation of:", A.id)
        e.solution(3)
        return(success)
    return(success)

#Chiamata del manager delle ambulanze in base alla priorità a
def Ambulance_allocation(Priority,env,e):
    completed=0
    a=0
    #print("Priority=",Priority)
    for i in Global_vars.indexes:
       #print(i)
       if Priority == 1 :
           if AmbulanceManager1(Global_vars.ambulances[a],env,e)==1:
               completed=1
               #print("completed with 1")
               break
       if Priority == 2 :
            if AmbulanceManager2(Global_vars.ambulances[a],env,e)==1:
               completed=1
               #print("completed with 2")
               break
       if Priority == 3 :
            if AmbulanceManager3(Global_vars.ambulances[a],env,e)==1:
               completed=1
               #print("completed with 3")
               break
       if Priority > 3:
           return 1
       a=a+1
    return completed
        
class Global_vars:
     # Simulation run time and warm-up (warm-up is time before results are
    # collected)
    
    warm_up = 2*60
    sim_duration = 24*60
    n=493
    namb=29
    #ambloc=LPM.LSCM()
    #ambloc=LPM.MLCP(29)
    
    alpha=1
    filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_\Figure','ambloc_DSM'+repr(alpha)+'.txt')
    data = pd.read_csv(filepath, sep=" ", header = None)
    ambloc=list(data[1])
    amblocnew=0
    
    #U and N_U normalised probability demand vector+ratio U/E,NU/E, tempi ecc
    totU=sum(D_U)
    totNU=sum(D_NU)
    totE=totU+totNU
    du=[]; dnu=[]
    for i in range(n):
        du.append(D_U[i]/totU)
        dnu.append(D_NU[i]/totNU)
    du=np.asarray(du)
    dnu=np.asarray(dnu)
    
    ratio=[totU/totE,totNU/totE]
    
    avgtime=((totE)/(365*24*60))**(-1)
    devtime=(avgtime)**(0.25)

    nrelocations=0
    # Average and standard deviation of time ambulances are out
    # with a patient)
    int_mean = 60
    int_sd = (int_mean)**(0.25)
    
    #create ambulances
    it=[]
    indexes=[]
    ambulances=[]
    number_of_ambs = 0
    for i in range(len(ambloc)):
        if ambloc[i]==1:
            it= Ambulance(i)
            ambulances.append(it)
            indexes.append(i)
            number_of_ambs=number_of_ambs+1
    
    
    # Lists used to store results
    time=[]
    availableambulances=[]
    e_priority=[]
    e_solution=[]

    # Set up dataframes to store results (will be transferred from lists)
    results = pd.DataFrame()

    # Set up counter for number of emergencies
    emergency_count1 = 0
    emergency_count2 = 0

class Model:
    
    def __init__(self):
        """constructor for initiating simpy simulation environment"""

        self.env = simpy.Environment()
        
         
    def build_em_results(self):
        """At end of model run, transfers results held in lists into a pandas
        DataFrame."""

        Global_vars.results['time'] = Global_vars.time
        Global_vars.results['availableambulances'] = Global_vars.availableambulances
        Global_vars.results["priority"]=Global_vars.e_priority
        Global_vars.results["solution"]=Global_vars.e_solution

        
        
    def chart(self):
        """At end of model run, plots model results using MatPlotLib."""
        
        fig = plt.figure(figsize=(12, 4.5), dpi=75)
        ax1 = fig.add_subplot(121)
        x = Global_vars.results['time']
        y = Global_vars.results['availableambulances']
        ax1.plot(x, y, label='Ambs available')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Available Ambulances')
        ax1.legend()
        ax1.grid(True, which='both', lw=1, ls='--', c='.75')
        
        ax2 = fig.add_subplot(122)  # 1 row, 3 cols, chart position 1
        x = range(Global_vars.emergency_count1+Global_vars.emergency_count2)
        markers = ['o', 'x']
        for priority in range(1, 3):
            x = (Global_vars.results[Global_vars.results['priority'] == priority].index)

            y = (Global_vars.results[Global_vars.results['priority'] ==priority]['solution'])

            ax2.scatter(x, y, marker=markers[priority-1], label='Priority ' + str(priority))

        ax2.set_xlabel('Emergency')
        ax2.set_ylabel('Time')
        ax2.legend()
        ax2.grid(True, which='both', lw=1, ls='--', c='.75')
        
        
        

        # Create plot
        plt.tight_layout(pad=2)
        plt.show()
        
    def metrics(self):
        
        PerfectCover1=len((Global_vars.results[(Global_vars.results['solution'] == 1) 
        & (Global_vars.results['priority'] == 1)]))/len(Global_vars.results[Global_vars.results['priority'] == 1])
    
        print("PerfectCover1 : ", PerfectCover1)
        
        PartialCover1=len(Global_vars.results[ (Global_vars.results['solution'] == 2) 
        & (Global_vars.results['priority'] == 1) ] )/len(Global_vars.results[Global_vars.results['priority'] == 1])
    
        print("PartialCover1 : ", PartialCover1)
        
        DecentCover1=PerfectCover1+PartialCover1
        
        print("DecentCover1  : ",DecentCover1)
        
        PerfectCover2=len((Global_vars.results[(Global_vars.results['solution'] != 3) 
        & (Global_vars.results['priority'] == 2)]))/len(Global_vars.results[Global_vars.results['priority'] == 2])
    
        print("PerfectCover2 : ", PerfectCover2)
        
        filepath = os.path.join(r'C:\Users\ffede\Google Drive\Reading_','Risultati.txt')
        with open(filepath, 'r') as file:
            data = file.readlines()
            
        data[c] = repr(modello)+ ',' +repr(seed) + ',' + repr(PerfectCover1) +',' + repr(PartialCover1)+',' + repr(PerfectCover2)
        
        # and write everything back
        with open(filepath, 'w') as file:
            file.writelines( data )
        
        file.close()
        
        
        
      
    def run(self):
        
        self.env.process(self.emergencygenerator())
        
        self.env.run(until=Global_vars.sim_duration)
        
        print("\n SIMULATION ENDED \n")
        
        self.build_em_results()
        self.chart()
        self.metrics()
                    
    def totherescue(self,e,env):

        #Chiamata delle ambulanze e soluzione emergenze
        """Se non c'è una soluzione con priorità n, si passa a cercare una
        soluzione con priorità n+1 ecc. Inserire caso per handling 
        eccezione: no ambulanze disponibili"""
        i=e.priority
        done=0
        while done == 0:
            done=Ambulance_allocation(i,env,e)
            i=i+1
        del i
        
        
        
        #guardo se le ambulanze occupate sono ora disponibili
        provv=0
        for i in range(len(Global_vars.indexes)):
            if Global_vars.ambulances[i].availability==0:
                Global_vars.ambulances[i].tryunfreeze(env)
            else:
                provv=provv+1
        
        if self.env.now > Global_vars.warm_up:
        
            Global_vars.availableambulances.append(provv)
            Global_vars.time.append(self.env.now)
            Global_vars.e_priority.append(e.priority)
            Global_vars.e_solution.append(e.time)
        
        yield self.env.timeout(e.duration)



    
    def emergencygenerator(self):
        """Generatore di emergenze: finchè il tempo della simulazione non giunge 
        al termine, genera emergenze ogni tot minuti, in base a una distribuzione
        esponenziale di parametro 1/(tempo medio di attesa tra emergenze)"""
        while True:
            #Initialise Emergency
            e = Emergency(self.env)
            
            Emergency.all_emergencies[e.id] = e

            
            self.env.process(self.totherescue(e,self.env))

            #next_emergency=random.normalvariate(Global_vars.avgtime,Global_vars.devtime)
            next_emergency=random.expovariate(1/Global_vars.avgtime)
            next_emergency = 0.01 if next_emergency < 0.01 \
            else next_emergency
            #print("next emergency: ", next_emergency)
            
            ##Cambiare tempo di attesa
            if len(Emergency.all_emergencies)>1:
                if Global_vars.namb>22:
                    Global_vars.alpha=1
                elif Global_vars.namb<23:
                    Global_vars.alpha=Global_vars.namb/23
                Global_vars.ambloc_new=LPM.DDSMt(Global_vars.namb,Global_vars.alpha,Global_vars.ambloc,300)
                if Global_vars.ambloc_new!=0:
                    Global_vars.ambloc=Global_vars.ambloc_new
                    Global_vars.nrelocations=Global_vars.nrelocations+1
                else:
                    True
                """
                for i in range(Global_vars.ambloc):
                    if Global_vars.amblocnew[i]!=Global_vars.ambloc[i]:
                        pr=[]
                        for i in range(Global_vars.namb):
                            pr.append[Global_vars.ambulances[i].id]
                        a=pr.index[i]
                        Global_vars.ambulances[a].position=Global_vars.amblocnew[i]
                        Global_vars.ambulances[a].stasis=8
                """    
                    
            yield self.env.timeout(next_emergency)
             
    #costruire data frame
    

class Emergency:
    all_emergencies={}
    def __init__(self,env):
        
        self.time_in = env.now
        print("time_in: ",self.time_in)
        
        self.id=Global_vars.emergency_count1+Global_vars.emergency_count2
        self.priority = np.random.choice(np.arange(1,3), p=Global_vars.ratio)
        
        if self.priority==1:
            self.zone=np.random.choice(np.arange(0, Global_vars.n), p=Global_vars.du)
            Global_vars.emergency_count1 += 1
        
        if self.priority==2:
            self.zone=np.random.choice(np.arange(0, Global_vars.n), p=Global_vars.dnu)
            Global_vars.emergency_count2 += 1

        self.duration=random.normalvariate(Global_vars.int_mean,Global_vars.int_sd)
        self.duration = 5 if self.duration < 5 \
            else self.duration
        #print("duration: ", self.duration)
        
        self.solved=0
        self.time=0
        print("Emergenza ",self.id)
    
    def solution(self,time):
        self.solved=1
        self.time=time
        

            
    
            
      
# Run model 
if __name__ == '__main__':
    # Initialise model environment
    model = Model()
    # Run model
    model.run()

    

#http://heather.cs.ucdavis.edu/~matloff/simcourse.html