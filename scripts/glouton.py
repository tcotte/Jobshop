import numpy as np    
import math
infini = math.inf


#############################################################################################################
# STP
# SPT (Shortest Processing Time) : donne priorité à la tâche la plus courte ;

def goutonne_stp (machines, durations, n, m):
    
    ressource = [[] for _ in range(m)] # matrice m*n
    list_job = [] #pour representation par job
    
    realisable = []
    #Initialisation : Déterminer l’ensemble des tâches réalisables (initialement, les premières tâches de tous les jobs) 
    for i in range(n):
        realisable.append((i,0))
        
    realisees = []
    
    while (len(realisable) != 0): #realisable peut redescendre à 0 et il reste des taches à realisées ??
        
        #Choisir une tâche dans cet ensemble, STP, la plus courte
        durees = []
        for (j,o) in realisable:
            duree = durations[j,o]
            durees.append(duree)
            
        next_t = realisable[np.argmin(np.array(durees))]
        
        #Placer cette tâche sur la ressource qu’elle demande 
        #(à la première place libre dans la représentation par ordre de passage)      
        k = machines[next_t]
        ressource[k].append(next_t)

        j,o = next_t
        list_job.append(j)
        
        #Mettre à jour l’ensemble des tâches réalisables
        # On dit qu’une tâche est réalisable si tous ses prédécesseurs ont été traités
        realisees.append(next_t)
        realisable.remove(next_t)
        if o<m-1: #un job contient m taches
            #print((j,o+1)) #debug
            realisable.append((j,o+1))
        
     
    #print(realisees) #debug
    #print(len(realisees)) #debug
    return list_job, ressource


############################################################################################""
# LRPT (Longest Remaining Processing Time) : donne la priorité à la tâche appartenant
# au job ayant la plus grande durée

def goutonne_lrtp (machines, durations, n, m):
    
    ressource = [[] for _ in range(m)] # matrice m*n
    list_job = [] #pour representation par job

    #on stocke à quelle tache on en est pour chacune des m ressources (max = n)
    state = [0]*m #au début 0
    
    realisable = []
    #Initialisation : Déterminer l’ensemble des tâches réalisables (initialement, les premières tâches de tous les jobs) 
    for i in range(n):
        realisable.append((i,0))
        
    realisees = []
    restantes = [[] for _ in range(n)] #taches restantes par job
    
    #initialisation
    for i in range(n):
        for j in range(m):
            restantes[i].append((i,j))
    
    
    while (len(realisable) != 0): #realisable peut redescendre à 0 et il reste des taches à realisées ??
        
        #Choisir une tâche dans cet ensemble, LRTP, tâche appartenant au job ayant la plus grande durée restante
        durees_restantes = [0]*n #pour chaque job
       
        for i in range(n):
            for j,o in restantes[i]:
                durees_restantes[i] += durations[j,o]
                
        max_j = np.argmax(np.array(durees_restantes))
        #print(durees_restantes) #debug
        #print(max_j) #debug
        
        for j,o in realisable:
            if j==max_j:     
                next_t = j,o
                #break #devrait etre ok
        #print(type(next_t)) #debug
        
        #Placer cette tâche sur la ressource qu’elle demande 
        #(à la première place libre dans la représentation par ordre de passage)      
        k = machines[next_t]
        ressource[k].append(next_t)

        j,o = next_t
        list_job.append(j)
        
        #Mettre à jour l’ensemble des tâches réalisables
        # On dit qu’une tâche est réalisable si tous ses prédécesseurs ont été traités
        realisees.append(next_t)
        realisable.remove(next_t)
        restantes[j].remove(next_t)
        if o<m-1: #un job contient m taches
            #print((j,o+1)) #debug
            realisable.append((j,o+1))
        
     
    #print(realisees) #debug
    #print(len(realisees)) #debug
    return list_job, ressource


####################################################################################################################
def gloutonne_est_spt(machines, durations, n, m):
    
    ressource = [[] for _ in range(m)] # matrice m*n
    list_job = [] #pour representation par job
    
    realisable = []
    
    #Initialisation : Déterminer l’ensemble des tâches réalisables (initialement, les premières tâches de tous les jobs) 
    for i in range(n):
        realisable.append((i,0))
        
    realisees = [[] for i in range(n)] #par job, on stocke date de debut de chaque tache
    
    
    while (len(realisable) != 0): #realisable peut redescendre à 0 et il reste des taches à realisées ??
        
        start_possible = [] #liste des dates de début possible ppour chaque tache realisable
        
        #On limites aux taches commencant au plus tot.
        #Trouver à quelle date peuvent commencer au plus tot chaque tache realisable
        for (j,o) in realisable:
            #machine libre
            mac = machines[j,o]
            if len(ressource[mac])>0:
                jm, om = ressource[mac][-1]
                mac_ready = realisees[jm][om] + durations[jm, om]
            if len(ressource[mac])==0:
                mac_ready = 0
            
            if o>0:
                #tache precedente finie
                fin_prec = realisees[j][o-1] + durations[j,o-1]
            if o==0:
                fin_prec = 0
            
            
            start_possible.append(max(mac_ready, fin_prec))
            
        start = min(start_possible)
        #indices = start_possible.index(start) #ne fonctionne pas, renvoie uniquement la première valeure
        choisies = [value for index, value in enumerate(realisable) if start_possible[index]==start]
        
        
        if len(choisies) !=1:
            #Choisir une tâche dans cet ensemble, STP, la plus courte
            durees = []
            for (j,o) in choisies:
                duree = durations[j,o]
                durees.append(duree)
            next_t = choisies[np.argmin(np.array(durees))]
            
        if len(choisies) ==1:
            next_t = choisies[0]
        
        #Placer cette tâche sur la ressource qu’elle demande 
        #(à la première place libre dans la représentation par ordre de passage)      
        k = machines[next_t]
        ressource[k].append(next_t)

        j,o = next_t
        list_job.append(j)
        
        #Mettre à jour l’ensemble des tâches réalisables
        # On dit qu’une tâche est réalisable si tous ses prédécesseurs ont été traités
        realisees[j].append(start) #
        
        realisable.remove(next_t)
        if o<m-1: #un job contient m taches
            #print((j,o+1)) #debug
            realisable.append((j,o+1))
        

    #print(realisees) #debug
    #print(len(realisees)) #debug
    return list_job, ressource


####################################################################################################""
def gloutonne_est_lrtp(machines, durations, n, m):
    
    ressource = [[] for _ in range(m)] # matrice m*n
    list_job = [] #pour representation par job

    #on stocke à quelle tache on en est pour chacune des m ressources (max = n)
    state = [0]*m #au début 0
    
    realisable = []
    #Initialisation : Déterminer l’ensemble des tâches réalisables (initialement, les premières tâches de tous les jobs) 
    for i in range(n):
        realisable.append((i,0))
        
    realisees = [[] for i in range(n)] #par job, on stocke date de debut de chaque tache
    restantes = [[] for _ in range(n)] #taches restantes par job
    
    #initialisation
    for i in range(n):
        for j in range(m):
            restantes[i].append((i,j))
    
    
    while (len(realisable) != 0): #realisable peut redescendre à 0 et il reste des taches à realisées ??
        
        
        start_possible = [] #liste des dates de début possible ppour chaque tache realisable
        
        #On limites aux taches commencant au plus tot.
        #Trouver à quelle date peuvent commencer au plus tot chaque tache realisable
        for (j,o) in realisable:
            #machine libre
            mac = machines[j,o]
            if len(ressource[mac])>0:
                jm, om = ressource[mac][-1]
                mac_ready = realisees[jm][om] + durations[jm, om]
            if len(ressource[mac])==0:
                mac_ready = 0
            
            if o>0:
                #tache precedente finie
                fin_prec = realisees[j][o-1] + durations[j,o-1]
            if o==0:
                fin_prec = 0
            
            
            start_possible.append(max(mac_ready, fin_prec))
            
        start = min(start_possible)
        #indices = start_possible.index(start) #ne fonctionne pas, renvoie uniquement la première valeure
        choisies = [value for index, value in enumerate(realisable) if start_possible[index]==start]
        #print(realisable) #debug
        #print(choisies) #debug
        
        if len(choisies)==1:
            next_t = choisies[0]
            
        if len(choisies)>1:
        
            #jobs correspondant à une tache choisie
            job_choisis = [j for j,o in choisies]
            
            #Choisir une tâche dans cet ensemble, LRTP, tâche appartenant au job ayant la plus grande durée restante
            durees_restantes = [0]* n #pour chaque job, choisi ou pas, 0 si non choisi       

            for i in job_choisis:
                for j,o in restantes[i]:
                    durees_restantes[i] += durations[j,o]

            max_j = np.argmax(np.array(durees_restantes))
            #print(durees_restantes) #debug
            #print(max_j) #debug

            for j,o in choisies:
                if j==max_j:     
                    next_t = j,o
                    #break #devrait etre ok
            #print(type(next_t)) #debug
            
        
        #Placer cette tâche sur la ressource qu’elle demande 
        #(à la première place libre dans la représentation par ordre de passage)      
        k = machines[next_t]
        ressource[k].append(next_t)

        j,o = next_t
        list_job.append(j)
        
        #Mettre à jour l’ensemble des tâches réalisables
        # On dit qu’une tâche est réalisable si tous ses prédécesseurs ont été traités
        realisees[j].append(start)
        #print(next_t) #debug
        realisable.remove(next_t)
        restantes[j].remove(next_t)
        if o<m-1: #un job contient m taches
            #print((j,o+1)) #debug
            realisable.append((j,o+1))
        
    #print(realisees) #debug
    #print(len(realisees)) #debug
    return list_job, ressource