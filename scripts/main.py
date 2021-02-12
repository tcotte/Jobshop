import numpy as np    
import os
import pandas as pd
import math
infini = math.inf
import general as ge
import glouton as gl

#get instances
f_list = os.listdir('../instances/')
file_list =[]
for f in f_list:
    f = "../instances/"+f
    file_list.append(f)
    
filename = file_list[0] # 0 pour abz5
#filename = '../instances/ft06'
print(filename)

machines, durations, n, m = ge.generate_instance(filename, 4) #we start at line 4 due to instance shape

list_job, ressource = ge.init_sol_resources_nocycle(n, m, machines) #initialisation random mais sans cycle (baséee sur repre job)

detail = ge.ressource_to_detaillee(ressource, n, m, durations, machines)
#print(detail)

makespan = ge.evaluate_detail(detail, n, m, machines, durations)
print("random sol makespan: ", makespan)

val = ge.validate_detail(detail, durations, machines, n, m)
#print(val)

ressource2, all_mach_times = ge.detail_to_ressource(detail, durations, machines, n, m)

#print(ressource2==ressouce) #check that we come back to initial ressource sol

ge.draw_gantt(n, m, machines, durations, detail)

#TODO chemin critique

#HEURISTIQUES GLOUTONNES
#Imlémentez les heuristiques STP et LRPT pour construire une solution représentée par ResourceOrder

### STP ###
list_job_stp, ressource_stp = gl.goutonne_stp (machines, durations, n, m)
detail_stp = ge.ressource_to_detaillee(ressource_stp, n, m, durations, machines)
print("stp: ", ge.evaluate_detail(detail_stp, n, m, machines, durations))

### LRTP ###
list_job_lrtp, ressource_lrtp = gl.goutonne_lrtp (machines, durations, n, m)
detail_lrtp = ge.ressource_to_detaillee(ressource_lrtp, n, m, durations, machines)
print("lrtp: ", ge.evaluate_detail(detail_lrtp, n, m, machines, durations))


#Améliorez ces heuristiques : EST-SPT et EST-LRPT
#Evaluez ces heuristiques sur les instances ft et la

### EST STP ###
list_job_est_stp, ressource_est_stp = gl.gloutonne_est_spt(machines, durations, n, m)
detail_est_stp = ge.ressource_to_detaillee(ressource_est_stp, n, m, durations, machines)
print("est stp: ", ge.evaluate_detail(detail_est_stp, n, m, machines, durations))

### EST LRTP ###
list_job_est_lrtp, ressource_est_lrtp = gl.gloutonne_est_lrtp(machines, durations, n, m)
detail_est_lrtp = ge.ressource_to_detaillee(ressource_est_lrtp, n, m, durations, machines)
print("est lrtp: ", ge.evaluate_detail(detail_est_lrtp, n, m, machines, durations))


#METHODES DE DESCENTES

