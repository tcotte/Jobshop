"""
    Module descent_solver.py
    Module permettant d'implémenter un solver par métohde de descente
"""
import time

import numpy as np
import scripts.general as ge
import math
import matplotlib.pyplot as plt
import glouton as gl


def blocks_of_critical_path(machines, critical_path):
    """
    Un bloc représente une sous-séquence du chemin critique de sorte à ce que toutes les tâches qu'il contient s'exécutent sur la même machine.
    Cette fonction identifie tous les blocs à partir d'une représentation ResourceOrder.
    Envisager la solution dans la représentation de ResourceOrder
     - machine 0 : (0,1) (1,2) (2,2)
     - machine 1 : (0,2) (2,1) (1,1)
     - machine 2 : ...
     Le bloc avec : machine = 1, firstTask= 0 et lastTask = 1
     Représente la séquence de tâches : [(0,2) (2,1)]
    :param machines: tableau contenant la liste des ressources
    :param critical_path: chemin critique
    :return: le séquence de tâches dans l'ordre chronologique : [[(0,2) (2,1)], [(0,3), (1,4)]
    """

    for i in critical_path:
        job = i[0]
        op = i[1]

    blocks = []
    i = 0
    memory = []

    while i < len(critical_path) - 1:
        current_task = critical_path[i]
        next_task = critical_path[i + 1]

        if get_ressource(machines, current_task[0], current_task[1]) == get_ressource(machines, next_task[0],
                                                                                      next_task[1]):
            memory.append(current_task)

        else:
            if len(memory) != 0:
                memory.append(current_task)
                blocks.append(memory)
                memory = []

        i += 1

    print("BLOCKS" + str(blocks))

    return blocks


def transform_blocks(blocks):
    """
        :param blocks: blocks où les tâches des listes des sous-séquences sont sous forme de tuples de taille 6
        :return: blocks où les tâches des listes des sous-séquences sont sous forme de tuples de taille 2 (job,op)
    """

    for ind_bloc, bloc in enumerate(blocks):
        for ind_task, task in enumerate(bloc):
            blocks[ind_bloc][ind_task] = transform_to_tuples(task)

    return blocks


def transform_to_tuples(task):
    """
        :param task: tâche sous forme de tuple de taille 6
        :return: tâche sous forme de tuple de taille 2 (job, op)
    """
    task_tuple = (task[1], task[2])
    return task_tuple


def get_ressource(machines, job, operation):
    """
     :param machines: tableau comportant la liste des machines
     :param job: job associé à une tâches
     :param operation: numéro d'opération associé à une tâche
     :return: ressource associée à la tache passée en paramètre à l'aide de "job" et "opération"
     """
    return machines[job, operation]


def swap(index, ressource, t1, t2):
    """
    :param index: numéro du bloc où deux positions doivent être échangées
    :param blocks: liste des blocks formés par le chemin critique
    :param t1: 1ère position d'échange
    :param t2: 2nde position d'échange
    :return: liste avec deux positions échagnées
    """
    ressource[index][t1], ressource[index][t2] = ressource[index][t2], ressource[index][t1]
    return ressource[index]


def neighbors(blocks, index):
    """
    Remarque : un bloc de taille 2, va renvoyer un voisin de taille : [(0,2) (2,1)]
               un bloc de taille 3 et +, va renvoyer 2 voisin : [[(0,2), (2,1), (1,3)], [(2,1), (1,3), (0,2)]
    :param blocks: liste des blocks formés par le chemin critique
    :param index: index du block à partir du quel nous renverrons un/des voisins
    :return: le ou les voisins associés à la taille du bloc.
    """
    sol = []
    if len(blocks[index]) == 2:
        sol = swap(index, blocks, 0, 1)

    if len(blocks[index]) > 2:
        original_block = blocks[index].copy()
        sol = [blocks[index], original_block]

        # sol.append(swap(index, orginal_blocks, 0, 1))
        # swap(index, orginal_blocks, 1, 0)
        # sol.append(swap(index, l, -2, -1))

        sol[0][0], sol[0][1] = sol[0][1], sol[0][0]
        sol[1][-2], sol[1][-1] = sol[1][-1], sol[1][-2]

    return sol


def apply_on(n, m, solution, machines, durations, block):
    """
    Appliquer l'échange sur l'ordre des ressources donné en le transformant en une nouvelle solution
    :param solution: solution admissible pour le moment
    :param machines: tableau comportant la liste des machines
    :param block: liste des blocks formés par le chemin critique
    :return: nouvelle solution générée à partir du meilleur voisin
    """
    if len(block[0]) == 2:
        return solution_generated_by_neighborhood(block, solution, machines)

    elif len(block[0]) > 2:
        best_index = best_neighbor(n, m, solution, block, machines, durations)
        print("index choose : ", best_index)
        return solution_generated_by_neighborhood(block[best_index], solution, machines)

    else:
        raise ValueError('A block can\'t be composed of one task')


def best_neighbor(n, m, solution_init, block, machines, durations):
    """
    :param n: nombre de jobs
    :param m: nombre de machines
    :param solution_init: solution initiale (générée par méthode gloutonne
    :param block: deux blocs générés grâce au voisinage
    :param machines: tableau comportant la liste des ressources nécessaires aux opérations
    :param durations: tableau comportant la liste des durées des opérations
    :return: l'index du bloc étant le meilleur voisin
    """
    makespan = math.inf
    best_solution = []
    best_index = 0
    solution = solution_init.copy()

    for c in range(2):
        solution_neighbor = solution_init.copy()
        block_neighbor = block[c]
        new_solution = solution_generated_by_neighborhood(block_neighbor, solution_neighbor, machines)

        detail = ge.ressource_to_detaillee(new_solution, n, m, durations, machines)
        makespan_neighbor = ge.evaluate_detail(detail, n, m, durations)

        if makespan_neighbor < makespan:
            makespan = makespan_neighbor
            best_solution = new_solution
            best_index = c

    return best_index


def solution_generated_by_neighborhood(block, solution, machines):
    """
    :param block: block généré par le voisinage (un seul bloc -> list)
    :param solution: solution étant admissible pour le moment
    :param machines: tableau comportant la liste des ressources nécessaires aux opérations
    :return: nouvelle solution généré à l'aide du bloc de voisinage
    """
    first_task = block[0]

    machine = get_ressource(machines, first_task[0], first_task[1])
    index_list = []
    for i in range(len(block)):
        index = solution[machine].index(block[i])
        solution[machine].pop(index)
        index_list.append(index)

    min_index = np.min(index_list)

    for ind, task in enumerate(block):
        solution[machine].insert(min_index + ind, task)

    return solution


def best_solution_loop(n, m, solution_init, blocks, machines, durations):
    best_makespan = math.inf
    best_solution = []

    for index, block in enumerate(blocks):
        swapped_block = neighbors(blocks, index)
        # swapped_block = neighbors(blocks, index)
        # best_nei = apply_on(n, m, solution_init, machines, durations, swapped_block)

        # swapped_block = apply_on(n, m, solution_init, machines, durations, block)
        # print("block ", index, " --> ", block, " ------ swapped ----- ", swapped_block)
        solution = apply_on(n, m, solution_init, machines, durations, swapped_block)
        detail = ge.ressource_to_detaillee(solution, n, m, durations, machines)
        new_makespan = ge.evaluate_detail(detail, n, m, durations)
        print("block ", index, " --> ", block, " ------ swapped ----- ", swapped_block, " MAKESPAN ", new_makespan)

        if new_makespan < best_makespan:
            best_solution = solution
            best_makespan = new_makespan

    return best_solution


def descent_solver(n, m, durations, init_sol, path, machines, early_stop=1):
    """
    Réalisation de la méthode de descente qui s'appuie sur l' exploration successive d’un voisinage de solutions.
    La méthode de descente s'arrête s'il n'y a pas d'amélioration de la solution durant un nombre d'itération égal à
    early_stop.
    :param n: nombre de jobs
    :param m: nombre des machines
    :param durations: tableau contenant les listes des durées
    :param init_sol: solution initiale, trouvée grâce à une méthode gloutonne
    :param path: chemin critique
    :param machines: tableau contenant les listes des machines
    :param early_stop: entier par défaut à 30
    :return: solution provenant de la méthode de descente
    """
    blocks = blocks_of_critical_path(machines, path)
    interval = len(blocks)
    print("BLOCKS --> " + str(blocks))

    counter = 0
    best_solution = init_sol

    detail_init = ge.ressource_to_detaillee(best_solution, n, m, durations, machines)
    makespan = ge.evaluate_detail(detail_init, n, m, durations)

    list_makespan = [makespan]

    while counter < early_stop:

        blocks, _ = extractBlocksCriticalPath(path, n, m, machines)
        print("BLOCK ", blocks)
        # solution = apply_on(n, m, solution, machines, durations, block)
        #
        # detail = ge.ressource_to_detaillee(solution, n, m, durations, machines)
        solution = best_solution_loop(n, m, best_solution, blocks, machines, durations)
        detail = ge.ressource_to_detaillee(solution, n, m, durations, machines)

        if ge.evaluate_detail(detail, n, m, durations) < makespan:

            makespan = ge.evaluate_detail(detail, n, m, durations)
            print("Change makespan ==> ", makespan)
            ge.display_detailed_ressource(solution)
            best_solution = solution
            print("solution ", best_solution)
            path = ge.critical_path(n, m, durations, detail, makespan)
            print(path)
            counter = 0
        else:
            print("No improvement")
            counter += 1

        list_makespan.append(makespan)

    plot_descent(list_makespan)
    return solution


def plot_descent(list_makespan):
    """
    :param list_makespan: list des makespan au cours de la descente
    :return: Plot l'évolution du makespan
    """
    x = np.arange(len(list_makespan))
    plt.plot(x, list_makespan)
    plt.title("Evolution du makespan au cours de la descente")
    plt.xlabel("Intéations")
    plt.ylabel("Makespan")
    plt.show()


########### MATHILDE #############

def extractBlocksCriticalPath(critiques, n, m, machines):
    blocks = []

    list_mac = []  # debug

    bloc = []

    prec_mac = machines[critiques[0]]  # initialisation
    bloc.append(critiques[0])

    list_mac.append(machines[critiques[0]])

    for i in range(1, len(critiques)):
        j, o = critiques[i]
        if prec_mac == machines[j, o]:
            bloc.append(critiques[i])
        else:
            blocks.append(bloc)  # on ajoute l'ancien bloc
            bloc = [critiques[i]]  # on en commence un nouveau

        prec_mac = machines[j, o]  # mise à jour machine prcedente
        list_mac.append(machines[critiques[i]])

    blocks.append(bloc)  # on ajoute le dernier bloc

    blocks = [b for b in blocks if len(b) > 1]  # on enleve les blocs de taille <2

    return blocks, list_mac


#####################################################################
# voisinage d'un bloc
def voisinage_bloc(bloc, ressource, machines):
    # on travaille sur un bloc, une seule machine est concernée
    j, o = bloc[0]
    mac = machines[j, o]
    print("bloc", bloc)

    new_sols = []  # on va stocker les nouvelles solutions associées aux voisins
    # par construction du voisinage, les nouvelles solutions sont valides,
    # car permutations sur taches d'une meme machine (et donc pas d'un meme job, pas de soucis de precedence)

    # voisinage d'un bloc
    liste_voisins = []

    # permutation 2 premières
    voisin1 = []
    voisin1.extend(bloc)
    voisin1[1], voisin1[0] = voisin1[0], voisin1[1]
    liste_voisins.append(voisin1)

    new_sol = ge.duplicate_ressource(ressource)
    i = new_sol[mac].index((bloc[0]))
    new_sol[mac][i], new_sol[mac][i + 1] = new_sol[mac][i + 1], new_sol[mac][i]
    new_sols.append(new_sol)

    if len(bloc) > 2:
        # permutation 2 dernières
        voisin2 = []
        voisin2.extend(bloc)
        voisin2[-1], voisin2[-2] = voisin2[-2], voisin2[-1]
        liste_voisins.append(voisin2)

        new_sol = ge.duplicate_ressource(ressource)
        i = new_sol[mac].index((bloc[-1]))
        new_sol[mac][i - 1], new_sol[mac][i] = new_sol[mac][i], new_sol[mac][i - 1]
        new_sols.append(new_sol)

    return liste_voisins, new_sols  # , bloc


#####################################################################
# Initialisation est_lrtp
def descente_solver(machines, durations, n, m, timeout=3600):  # timeout en secondes
    # initialisation
    list_job, best_sol = gl.gloutonne_est_lrtp(machines, durations, n, m)

    best_detail = ge.ressource_to_detaillee(best_sol, n, m, durations, machines)
    meilleure = ge.evaluate_detail(best_detail, n, m,  durations)  # memo meilleure sol
    critiques, times = ge.chemin_critique(best_detail, n, m, machines, durations, best_sol)

    start = time.time()
    while time.time() < start + timeout:
        # blocks du chemin critique
        blocks, list_mac = extractBlocksCriticalPath(critiques, n, m, machines)

        # explorer voisinages successifs
        # voisinage complet d'une solution est l'ensemble des voisinages de bloc
        voisinage_complet = []
        for i in range(len(blocks)):
            b = blocks[i]
            liste_voisins, new_sols = voisinage_bloc(b, best_sol, machines)
            voisinage_complet.extend(new_sols)

        # choisir meilleur voisin
        best_voisin = math.inf
        for s in voisinage_complet:
            print(s)
            new_detail = ge.ressource_to_detaillee(s, n, m, durations, machines)
            new_eval = ge.evaluate_detail(new_detail, n, m, durations)  # memo meilleure sol
            if new_eval < best_voisin:
                best_voisin = new_eval
                best_voisin_sol = s
                best_voisin_detail = new_detail

        # si meilleur que solution precedente, update meilleure sol
        if best_voisin < meilleure:
            meilleure = best_voisin
            best_sol = best_voisin_sol
            best_detail = best_voisin_detail
            critiques, times = ge.chemin_critique(best_detail, n, m, machines, durations, best_sol)

        # arret si pas d'amelioration ou time-out
        else:  # best_voisin_eval >= meilleure:
            print("no improvement")
            break

    return meilleure, best_sol
