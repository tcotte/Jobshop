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
    # print(content)
    lines = content.split("\n")

    array = []

    for i in lines[start:]:
        numbers = i.split(" ")
        while numbers.count('') > 0:
            numbers.remove('')
        for j in range(len(numbers)):
            numbers[j] = int(numbers[j])
        # print(numbers)
        if numbers != []:
            array.append(numbers)

    n = array[0][0]  # number of jobs
    m = array[0][1]  # number of machines

    machines = np.matrix(array[1:])[:, ::2]

    durations = np.matrix(array[1:])[:, 1::2]

    return machines, durations, n, m


#####################################################################
# init avec job representation
# permutation avec m valeures pour chaque job (n jobs)
def init_job(n, m):
    list_job = []
    for i in range(n):
        lis = [i] * m
        list_job.extend(lis)

    list_job = np.random.permutation(np.array(list_job))
    list_job.tolist()
    return list_job


#####################################################################
# une solution de type ordre de passage sur les ressources represente:
# pour chaque index l'odre dans lequel réaliser les diff op
# matrice de taille m (nbre index) * n (nombres de job)
# sachant que chaque job contient exactement 1 operation par index

# solution random mais sans cycle car issue de job representation

def init_sol_resources_nocycle(n, m, machines):
    ressource = [[] for _ in range(m)]  # matrice m*n

    list_job = init_job(n, m)  # representation job aléatoire
    print("liste ordonnée job", list_job)

    # on stocke à quelle tache on en est pour chacun des n job (max = m)
    state = [0] * n  # au début 0 pour chaque mach

    for j in list_job:
        # trouver la index utilisée pour le job j à la kème tache (k=state[j])
        mac = machines[j, state[j]]
        # on peut remplir ressource
        ressource[mac].append((j, state[j]))

        state[j] += 1

    return list_job, ressource


###################################################################################################
# on va passer de la representation par ressource à la representation détaillée
# la representation détaillée: matrice de n lignes (nombre de job) et m colonnes (nbre machines)
# la jeme colonne correspond a la jieme op pour le job en question
# chaque case contient la date de début de l'op correspondante

def ressource_to_detaillee(tupl_l, n, m, durations, machines):
    # on stocke à quelle tache en est chaque index (max = n-1)
    state = [0 for k in range(m)]  # au début 0 pour chaque index

    # on créé la matrice qu'on essaie de créer, la representation détailléee
    detail = [[infini] * m for _ in range(n)]  # initialisation à +inf

    it = 0

    #  "on recommence à chaque fois qu'on avance..""
    while (max([sum(detail[i]) for i in range(n)]) >= infini):  # and (iter<5000)

        move_c = 0  # on regarde si on a réussi à remplir au moins une case dans la dernière itération
        it += 1

        # on remplit colonne par colonne la représentation détaillée
        for j in range(m):
            for i in range(n):

                # on s'interesse à la tache (i,j) la jème tache pour le job i

                if detail[i][j] == infini:  # sinon pas besoin de s'interesser à cette tache

                    # tps auquel la tache precedente pour le job sera finie
                    if j == 0:
                        prec = 0
                    if j > 0:
                        prec = detail[i][j - 1] + durations[i, j - 1]

                    # print("prec job: ", prec)

                    # on peut commencer seulement si index necessaire pour la tache est libre
                    # index necessaire -> regarder matrice machines

                    machine_used = machines[i, j]
                    st = state[machine_used]  # quelle colonne de ressource representation est la suivante

                    job, num_op = tupl_l[machine_used][st]

                    if job != i:
                        # on ne peut pas faire la tache desuite, la index a une autre tache de prévue
                        mac = infini
                    if job == i:
                        if st == 0:  # si st = 0, 1ère tache, la index est prete
                            mac = 0
                        if st != 0:
                            # la index fnit sa tache precedente puis c'est le tour de notre tache
                            prec_j, prec_tache_machine = tupl_l[machine_used][st - 1]
                            mac = detail[prec_j][prec_tache_machine] + durations[prec_j, prec_tache_machine]

                    # print("prec ressource: ", mac)
                    startdate = max(mac, prec)
                    detail[i][j] = startdate

                    # mise à jour de state
                    if startdate < infini:
                        state[machine_used] += 1
                        move_c += 1  # on a remplit une case

        # print("move after colonne : ", move_c)

        move_l = 0
        if (move_c + move_l) == 0:
            print("no move")
            break

    return detail


##############################################################
def evaluate_detail(detail, n, m, durations):
    fins = []
    for i in range(n):
        fin = detail[i][m - 1] + durations[i, m - 1]
        fins.append(fin)

    return max(fins)


###############################################################
def validate_detail(detail, durations, machines, n, m):
    val = True  # initialisation à valider = True, si une contrainte est violée, on passe à False et on arrete

    # precedence
    for i in range(n):
        for j in range(m - 1):
            if detail[i][j + 1] < detail[i][j] + durations[i, j]:
                print("not correct precedence for ligne ", i, 'colonne: ', j)
                val = False
                break

    # index ne peut traiter qu'une tache à la fois
    # on verifie qu'un index ne fait qu'une tache à la fois

    for k in range(m):
        # retrouver toutes les taches de la index et stocker les startdates
        list_start = []
        list_start_durations = []
        for i in range(n):
            j = machines[[i], :].tolist()[0].index(k)  # j contient le numéro d'op
            start = detail[i][j]
            list_start.append((start, j))
        # les ordonner par startdate
        list_start = sorted(list_start, key=lambda tache: tache[0])
        for s, j in list_start:
            end = s + durations[i, j]
            list_start_durations.append((start, end))

        # verifier que startdate+duration<nextstartdate
        for i in range(len(list_start_durations) - 1):
            s = list_start_durations[i + 1]  # date de début de la prochaine tache
            e = list_start_durations[i]
            if s < e:
                print("not correct, plus d'une tache à la fois pour index ", k, 'start: ', s)
                val = False
                break

    return val


###########################################################################################
def detail_to_ressource(detail, durations, machines, n, m):
    ressource = []  # la resprésentation ressource associée
    all_mach_times = []
    for k in range(m):
        # retrouver toutes les taches de la index et stocker les startdates
        list_taches = []
        list_start = []
        list_start_durations = []
        for i in range(n):
            j = machines[[i], :].tolist()[0].index(k)  # j contient le numéro d'op
            start = detail[i][j]
            tripl = (start, i, j)
            list_start.append(tripl)
        # les ordonner par startdate
        list_start = sorted(list_start, key=lambda tache: tache[0])

        for k in range(n):
            s, i, j = list_start[k]
            end = s + durations[i, j]
            tupl = (i, j)
            list_taches.append(tupl)  # une tache est un tuple (job,numero_op)
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
            np_repr[i, j] = detail[i][j]

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

def end_time(start_time, duration):
    return start_time + duration


############################################################
# TODO chemin critique, calcul et display
def critical_path(nb_jobs, nb_machines, durations, start_time, makespan, machines, ressource):
    critical_tasks = []
    end_list = []
    durations = durations.tolist()

    for i in range(nb_jobs):
        for j in range(nb_machines):
            end_list.append(
                ["Job " + str(i) + " /op " + str(j), i, j, durations[i][j], start_time[i][j],
                 end_time(start_time[i][j], durations[i][j])])

    endTime = int(makespan)

    path = []
    path.append(in_list(endTime, end_list))

    while endTime != 0:
        current_task = path[-1]

        latest_predecessor = []

        # get previous task in the job
        if current_task[2] > 0:
            task_pred_on_job = get_pred_task(current_task[1], current_task[2] - 1, end_list)

            # if it was the delaying task, save it to predecessor
            if task_pred_on_job[5] == current_task[4]:
                latest_predecessor = task_pred_on_job

        # if there is not predecessor currently, get previous task of the machine
        if not latest_predecessor:
            machine = get_ressource(machines, current_task[1], current_task[2])
            index_previous_task = ressource[machine].index((current_task[1], current_task[2])) - 1
            pred_task_machine = get_pred_task(ressource[machine][index_previous_task][0],
                                              ressource[machine][index_previous_task][1], end_list)

            # if it was the delaying task, save it to predecessor
            if pred_task_machine[5] == current_task[4]:
                latest_predecessor = pred_task_machine

        path.append(latest_predecessor)

        if latest_predecessor[4] == 0:
            break

        endTime = latest_predecessor[5]

    path.reverse()

    return get_tuples(path)


def get_ressource(machines, job, operation):
    """
     :param machines: tableau comportant la liste des machines
     :param job: job associé à une tâches
     :param operation: numéro d'opération associé à une tâche
     :return: ressource associée à la tache passée en paramètre à l'aide de "job" et "opération"
     """
    return machines[job, operation]


def in_list(c, classes):
    for i, sublist in enumerate(classes):
        if c == sublist[5]:
            return sublist
    return -1


def get_pred_task(c, d, classes):
    for i, sublist in enumerate(classes):
        if c == sublist[1] and d == sublist[2]:
            return sublist
    return -1


def get_tuples(path):
    blocks = []
    for i in path:
        blocks.append((i[1], i[2]))
    return blocks


############################################################

def display_detailed_ressource(ressource):
    for i, val in enumerate(ressource):
        print("index " + str(i) + " : " + str(val))


############################################################ MATHILDE

def chemin_critique(detail, n, m, machines, durations, ressource):
    # Calculer le chemin critique et retourner la liste de tâches qui le compose
    makespan = evaluate_detail(detail, n, m, durations)

    critiques = []  # contient des taches (j,o)
    times = []  # contient les endtimes le long du chemin critique

    longest_time = makespan
    times.append(makespan)

    # initialisation, on commence par la fin
    for i in range(n):
        if detail[i][m - 1] + durations[i, m - 1] == longest_time:
            # tache i, m-1 est sur chemin_critique
            tache = (i, m - 1)
            critiques.append(tache)
            longest_time -= durations[i, m - 1]
            times.insert(0, longest_time)
            break  # on ajoute qu'un élément si égalité

    while longest_time != 0:

        # print(critiques) #debug
        last = critiques[0]

        j, o = last
        mac = machines[j, o]

        # pred_job = [] #tache precedente du job et precedente de la machine

        # tache precedente du job
        if detail[j][o - 1] + durations[j, o - 1] == detail[j][o]:
            tache = (j, o - 1)  # debug
            critiques.insert(0, tache)
            longest_time -= durations[j, o - 1]
            times.insert(0, longest_time)
            # print('job prec: ', critiques)

        else:
            # tache precedente de la machine
            mac_index = ressource[mac].index(last)
            jm, om = ressource[mac][mac_index - 1]  # tache recedente machine

            if detail[jm][om] + durations[jm, om] == detail[j][o]:
                critiques.insert(0, (jm, om))
                longest_time -= durations[jm, om]
                times.insert(0, longest_time)
                # print('machine prec: ', critiques)

            else:
                print("no tache correspondante, probleme?")

    # Methode PERT? TODO

    return critiques, times


#############################################################################
def duplicate_ressource(resource):
    new_resource = []
    for r in resource:
        r_new = []
        for t in r:
            r_new.append(t)
        new_resource.append(r_new)

    return new_resource
