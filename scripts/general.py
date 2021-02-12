import numpy as np
import pandas as pd
import math
infini = math.inf
from datetime import date
from datetime import timedelta
from plotly.figure_factory import create_gantt



def generate_instance(filename, start):
    f = open(filename, "r")
    content = f.read()
    f.close()
    #print(content)
    lines = content.split("\n")

    array = []

    for i in lines[start:]:
        numbers = i.split(" ")
        while numbers.count('') >0:
            numbers.remove('')
        for j in range(len(numbers)):
            numbers[j] = int(numbers[j])
        #print(numbers)
        if numbers != []:
            array.append(numbers)

    n = array[0][0] #number of jobs
    m = array[0][1] #number of machines

    machines = np.matrix(array[1:])[:,::2]
    
    durations = np.matrix(array[1:])[:,1::2]

    return machines, durations, n, m

#####################################################################
#init avec job representation
#permutation avec m valeures pour chaque job (n jobs)
def init_job(n,m):
    list_job = []
    for i in range(n):
        lis = [i] * m
        list_job.extend(lis)

    list_job = np.random.permutation(np.array(list_job))
    list_job.tolist()
    return list_job


#####################################################################
# une solution de type ordre de passage sur les ressources represente:
# pour chaque machine l'odre dans lequel réaliser les diff op
# matrice de taille m (nbre machine) * n (nombres de job)
# sachant que chaque job contient exactement 1 operation par machine

#solution random mais sans cycle car issue de job representation

def init_sol_resources_nocycle(n,m, machines):
    
    ressource = [[] for _ in range(m)] # matrice m*n
    
    list_job = init_job(n,m) #representation job aléatoire
    print("liste ordonnée job", list_job)
    
    #on stocke à quelle tache on en est pour chacun des n job (max = m)
    state = [0]*n #au début 0 pour chaque mach
    
    for j in list_job:
        #trouver la machine utilisée pour le job j à la kème tache (k=state[j])
        mac = machines[j,state[j]]
        #on peut remplir ressource
        ressource[mac].append((j,state[j]))
        
        state[j]+=1      
    
    
    return list_job, ressource


###################################################################################################
# on va passer de la representation par ressource à la representation détaillée
# la representation détaillée: matrice de n lignes (nombre de job) et m colonnes (nbre machines)
# la jeme colonne correspond a la jieme op pour le job en question
# chaque case contient la date de début de l'op correspondante

def ressource_to_detaillee(tupl_l, n, m, durations, machines):
       
    #on stocke à quelle tache en est chaque machine (max = n-1)
    state = [0 for k in range(m)] #au début 0 pour chaque machine
    
    #on créé la matrice qu'on essaie de créer, la representation détailléee
    detail = [[infini] * m for _ in range(n)] #initialisation à +inf
    
    it =  0
    
    #  "on recommence à chaque fois qu'on avance..""
    while (max([sum(detail[i]) for i in range(n)])>=infini): # and (iter<5000)
        
        move_c = 0 #on regarde si on a réussi à remplir au moins une case dans la dernière itération
        it+=1

        
        #on remplit colonne par colonne la représentation détaillée
        for j in range(m):
            for i in range(n):

                #on s'interesse à la tache (i,j) la jème tache pour le job i

                if detail[i][j] == infini: #sinon pas besoin de s'interesser à cette tache
                
                    #tps auquel la tache precedente pour le job sera finie
                    if j==0:
                        prec = 0
                    if j>0:
                        prec = detail[i][j-1] + durations[i,j-1]

                    #print("prec job: ", prec)

                    #on peut commencer seulement si machine necessaire pour la tache est libre
                    #machine necessaire -> regarder matrice machines

                    machine_used = machines[i,j]
                    st = state[machine_used] #quelle colonne de ressource representation est la suivante

                    job, num_op = tupl_l[machine_used][st]
   
                    if job != i:
                        #on ne peut pas faire la tache desuite, la machine a une autre tache de prévue
                        mac = infini
                    if job ==i:
                        if st ==0: #si st = 0, 1ère tache, la machine est prete
                            mac = 0
                        if st!=0:
                        #la machine fnit sa tache precedente puis c'est le tour de notre tache
                            prec_j, prec_tache_machine = tupl_l[machine_used][st-1]
                            mac = detail[prec_j] [prec_tache_machine] + durations[prec_j, prec_tache_machine]

                    #print("prec ressource: ", mac)
                    startdate = max(mac,prec)
                    detail[i][j] = startdate

                    #mise à jour de state
                    if startdate < infini:
                        state[machine_used]+=1
                        move_c += 1 #on a remplit une case
                        
        #print("move after colonne : ", move_c)

        move_l = 0
        if (move_c + move_l) ==0:
            print("no move")
            break

            
    return detail

##############################################################
def evaluate_detail(detail, n, m, machines, durations):
    fins = []
    for i in range(n):
        fin = detail[i][m-1]
        fins.append(fin)
    
    return max(fins)


###############################################################
def validate_detail(detail, durations, machines, n, m):
    
    val = True #initialisation à valider = True, si une contrainte est violée, on passe à False et on arrete
    
    #precedence
    for i in range(n):
        for j in range(m-1):   
            if detail[i][j+1]<detail[i][j]+durations[i,j]:
                print("not correct precedence for ligne ", i, 'colonne: ', j)
                val = False
                break
    

    
    #machine ne peut traiter qu'une tache à la fois
    #on verifie qu'un machine ne fait qu'une tache à la fois
    
    for k in range(m):
        #retrouver toutes les taches de la machine et stocker les startdates
        list_start = []
        list_start_durations = []
        for i in range(n):
            j = machines[[i],:].tolist()[0].index(k) #j contient le numéro d'op
            start = detail[i][j]
            list_start.append((start,j))
        #les ordonner par startdate  
        list_start = sorted(list_start, key=lambda tache: tache[0])
        for s,j in list_start:
            end = s + durations[i,j]
            list_start_durations.append((start, end))
          
    
        #verifier que startdate+duration<nextstartdate
        for i in range(len(list_start_durations)-1):
            s = list_start_durations[i+1] #date de début de la prochaine tache
            e = list_start_durations[i]
            if s<e:
                print("not correct, plus d'une tache à la fois pour machine ", k, 'start: ', s)
                val = False      
                break
    
    
    return val

###########################################################################################
def detail_to_ressource(detail, durations, machines, n, m):
       
    ressource = [] #la resprésentation ressource associée
    all_mach_times = []
    for k in range(m):
        #retrouver toutes les taches de la machine et stocker les startdates
        list_taches = []
        list_start = []
        list_start_durations = []
        for i in range(n):
            j = machines[[i],:].tolist()[0].index(k) #j contient le numéro d'op
            start = detail[i][j]
            tripl = (start,i,j)
            list_start.append(tripl)
        #les ordonner par startdate  
        list_start = sorted(list_start, key=lambda tache: tache[0])
        
        for k in range(n):
            s,i,j = list_start[k]
            end = s + durations[i,j]
            tupl = (i,j)
            list_taches.append(tupl) #une tache est un tuple (job,numero_op)
            list_start_durations.append((start, end))
    
        
        ressource.append(list_taches) 
        all_mach_times.append(list_start_durations)       
    
    
    
    return ressource, all_mach_times

#####################################################
def list_to_npmatrix(detail):
    n = len(detail)
    m = len(detail[0])
    np_repr = np.zeros((n, m))
    
    for i in range(n):
        for j in range(m):
            np_repr[i,j] = detail[i][j]
    
    return np_repr

#####################################################################
def draw_gantt(nb_jobs, nb_machines, machines, durations, detail):
    
    representation = list_to_npmatrix(detail)
    
    today = date.today()
    list_gantt = []
    for i in range(nb_jobs):
        for j in range(nb_machines):
            list_gantt.append(['r' + str(machines[i, j] + 1),
                               str(today + timedelta(days=representation[i][j])),
                               str(today + timedelta(days=representation[i][j]) + timedelta(days=int(durations[i, j]))),
                               'Job' + str(i + 1)])

    df = pd.DataFrame(list_gantt,
                      columns=['Task', 'Start', 'Finish', 'Resource'])

    fig = create_gantt(df, index_col='Resource', show_colorbar=True,
                       group_tasks=True)

    fig.show()
    
############################################################
#TODO chemin critique, calcul et display
