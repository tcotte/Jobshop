"""
    Module descent_solver.py
    Module permettant d'implémenter un solver par méthode de descente
"""
import time
import scripts.glouton as gl
import numpy as np
import scripts.general as ge
import math
import matplotlib.pyplot as plt


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


def blocks_from_critical_path(critical_path, machines):
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
    blocks = []
    bloc = []

    precedent_machine = machines[critical_path[0]]  # initialisation
    bloc.append(critical_path[0])

    for task in critical_path:
        if precedent_machine == ge.get_ressource(machines, task[0], task[1]):
            bloc.append(task)
        else:
            blocks.append(bloc)  # on ajoute l'ancien bloc
            bloc = [task]  # on en commence un nouveau

        precedent_machine = ge.get_ressource(machines, task[0], task[1])  # mise à jour machine prcedente

    blocks.append(bloc)  # on ajoute le dernier bloc

    blocks = [b for b in blocks if len(b) > 1]  # on enleve les blocs de taille <2

    return blocks


#####################################################################
# voisinage d'un bloc
def solution_generated_by_neighborhood(bloc, ressource, machines):
    """
    :param bloc: block généré par le voisinage (un seul bloc -> list)
    :param ressource: solution étant admissible pour le moment
    :param machines: tableau comportant la liste des ressources nécessaires aux opérations
    :return: nouvelle(s) solution(s) générée(s) à l'aide du bloc de voisinage
    """
    machine = ge.get_ressource(machines, bloc[0][0], bloc[0][1])
    print("bloc", bloc)

    list_solutions = []  # on va stocker les nouvelles solutions associées aux voisins
    # par construction du voisinage, les nouvelles solutions sont valides,
    # car permutations sur taches d'une meme machine (et donc pas d'un meme job, pas de soucis de precedence)

    # voisinage d'un bloc
    list_neighbors = []

    # permutation 2 premières
    neighbor_1 = []
    neighbor_1.extend(bloc)
    neighbor_1[1], neighbor_1[0] = neighbor_1[0], neighbor_1[1]
    list_neighbors.append(neighbor_1)

    new_solution = ge.duplicate_ressource(ressource)
    index = new_solution[machine].index((bloc[0]))
    new_solution[machine][index], new_solution[machine][index + 1] = new_solution[machine][index + 1], \
                                                                     new_solution[machine][index]
    list_solutions.append(new_solution)

    if len(bloc) > 2:
        # permutation 2 dernières
        neighbor_2 = []
        neighbor_2.extend(bloc)
        neighbor_2[-1], neighbor_2[-2] = neighbor_2[-2], neighbor_2[-1]
        list_neighbors.append(neighbor_2)

        new_solution = ge.duplicate_ressource(ressource)
        index = new_solution[machine].index((bloc[-1]))
        new_solution[machine][index - 1], new_solution[machine][index] = new_solution[machine][index], \
                                                                         new_solution[machine][index - 1]
        list_solutions.append(new_solution)

    return list_solutions


#####################################################################
# Initialisation est_lrtp
def descent_solver(machines, durations, n, m, solution, timeout=3600, plot=True):  # timeout en secondes
    """
    Réalisation de la méthode de descente qui s'appuie sur l' exploration successive d’un voisinage de solutions.
    La méthode de descente s'arrête s'il n'y a pas d'amélioration de la solution à l'itération suivante ou que le timeout
    est atteint
    :param n: nombre de jobs
    :param m: nombre des machines
    :param durations: tableau contenant les listes des durées
    :param solution: solution initiale, trouvée grâce à un autre solveur
    :param machines: tableau contenant les listes des machines
    :param timeout: temps maximum en secondes
    :return: Meilleure solution trouvée par la méthode de descente
    """
    best_solution = solution
    best_detail = ge.ressource_to_detaillee(best_solution, n, m, durations, machines)
    makespan = ge.evaluate_detail(best_detail, n, m, durations)  # memo makespan sol
    path = ge.critical_path(n, m, durations, best_detail, makespan, machines, best_solution)
    list_makespan = [makespan]

    start = time.time()
    while time.time() < start + timeout:
        # blocks du chemin critique
        blocks = blocks_from_critical_path(path, machines)

        # list des solutions atteintes par voisinage
        all_neighbors = return_all_neighbors(blocks, best_solution, machines)

        # choisir meilleur voisin
        best_voisin, best_voisin_sol, best_voisin_detail = choose_best_neighbor(all_neighbors, n, m, durations,
                                                                                machines)

        # si meilleur que solution precedente, mise à jour de la solution
        if best_voisin < makespan:
            makespan = best_voisin
            list_makespan.append(makespan)
            best_solution = best_voisin_sol
            best_detail = best_voisin_detail
            path = ge.critical_path(n, m, durations, best_detail, makespan, machines, best_solution)

        # arret si pas d'amelioration ou time-out
        else:
            print("no improvement")
            break

    if plot: plot_descent(list_makespan)
    return makespan, best_solution


def return_all_neighbors(blocks, solution, machines):
    """
    :param blocks: liste de tous les blocs
    :param solution: solution en cours d'exploitation
    :param machines: liste des machines
    :return: list des solutions atteintes par voisinage
    """
    all_neighbors = []
    for i in range(len(blocks)):
        b = blocks[i]
        new_solution = solution_generated_by_neighborhood(b, solution, machines)
        print("new sols ", new_solution)
        all_neighbors.extend(new_solution)
    return all_neighbors


def choose_best_neighbor(all_neighbors, n, m, durations, machines):
    """
    :param all_neighbors: liste de tous les voisins
    :param n:
    :param m:
    :param durations:
    :param machines:
    :return: meilleur voisin : makespan, solution, détaille des horaires de la solution
    """
    best_neighbor = math.inf
    for solution in all_neighbors:
        new_detail = ge.ressource_to_detaillee(solution, n, m, durations, machines)
        new_eval = ge.evaluate_detail(new_detail, n, m, durations)  # memo makespan sol
        if new_eval < best_neighbor:
            best_neighbor = new_eval
            best_neighbor_solution = solution
            best_neighbor_detail = new_detail
    return best_neighbor, best_neighbor_solution, best_neighbor_detail


#############################################################
#############################################################
def voisinage_bloc_taboo(bloc, ressource, machines):
    # on travaille sur un bloc, une seule machine est concernée
    j, o = bloc[0]
    mac = machines[j, o]
    # print("bloc", bloc)

    new_sols = []  # on va stocker les nouvelles solutions associées aux voisins
    # par construction du voisinage, les nouvelles solutions sont valides, *** TODO
    # car permutations sur taches d'une meme machine (et donc pas d'un meme job, pas de soucis de precedence)

    # voisinage d'un bloc
    liste_voisins = []
    liste_interdit = []

    # permutation 2 premières
    voisin1 = []
    voisin1.extend(bloc)
    interdit = (voisin1[0][0], voisin1[1][0])  # on ne stocke que le numér de job, pas le numero d'op
    voisin1[1], voisin1[0] = voisin1[0], voisin1[1]
    liste_voisins.append(voisin1)
    liste_interdit.append(interdit)

    new_sol = ge.duplicate_ressource(ressource)
    i = new_sol[mac].index((bloc[0]))
    new_sol[mac][i], new_sol[mac][i + 1] = new_sol[mac][i + 1], new_sol[mac][i]
    new_sols.append(new_sol)

    if len(bloc) > 2:
        # permutation 2 dernières
        voisin2 = []
        voisin2.extend(bloc)
        interdit = (voisin2[-2][0], voisin2[-1][0])
        voisin2[-1], voisin2[-2] = voisin2[-2], voisin2[-1]
        liste_voisins.append(voisin2)
        liste_interdit.append(interdit)

        new_sol = ge.duplicate_ressource(ressource)
        i = new_sol[mac].index((bloc[-1]))
        new_sol[mac][i - 1], new_sol[mac][i] = new_sol[mac][i], new_sol[mac][i - 1]
        new_sols.append(new_sol)

    return liste_voisins, new_sols, liste_interdit


#########################################################################

def taboo_solver(machines, durations, n, m, timeout, dureeTaboo, maxiter):  # timeout en secondes

    # initialisation
    list_job, current_sol = gl.gloutonne_est_lrtp(machines, durations, n, m)

    current_detail = ge.ressource_to_detaillee(current_sol, n, m, durations, machines)
    meilleure = ge.evaluate_detail(current_detail, n, m, durations)  # memo meilleure sol
    critiques, times = ge.chemin_critique(current_detail, n, m, machines, durations, current_sol)

    # Structure pour stocker les permutations taboo

    # for all machines
    # On crée une "matrice" avec toutes les taches associées à la machine, une par job (n)

    # on note pour chaque permutation le numéro d’itérations à partir de laquelle le mouvement est autorisé
    # initialisation à 0, aucune permutation n'est interdite
    listes_taboo = [[[0] * n] * n] * m
    # attention, le nombre de blocks va évoluer au cours des changements de solution avec la méthode tabou

    start = time.time()

    it = 0

    while (time.time() < start + timeout and it < maxiter):

        it += 1

        # blocks du chemin critique
        blocks, list_mac = extractBlocksCriticalPath(critiques, n, m, machines)

        # print(critiques)
        # print(blocks)

        # explorer voisinages successifs
        # voisinage complet d'une solution est l'ensemble des voisinages de chaque bloc

        best_voisin = math.inf
        # on va explorer pour tous les blocks, tous les voisins, s'ils sont non tabous on les évalue,
        # on stocke le meilleur voisin non tabou, qui deviendra la solution courrante à la fin de l'exploration de tous blocks
        # la permutation inverse au voisin choisi sera inerdite pour dureeTaboo itérations

        for i in range(len(blocks)):
            b = blocks[i]
            liste_voisins, new_sols, liste_interdit = voisinage_bloc_taboo(b, current_sol, machines)

            # trouver la machine pour ce bloc, pour pouvoir avoir la liste de taboo associée
            # j, o = b[0]
            mac = machines[b[0]]

            for v in range(len(liste_voisins)):
                # print(liste_interdit[v]) #debug
                # print(i) #debug

                # voisins exploré seulement si permutation possible ( <it )
                # la permutation faite est l'inverse de l'interdite
                if listes_taboo[mac][liste_interdit[v][1]][liste_interdit[v][0]] < it:  # tocheck

                    s = new_sols[v]
                    new_detail = ge.ressource_to_detaillee(s, n, m, durations, machines)
                    new_eval = ge.evaluate_detail(new_detail, n, m,  durations)  # memo meilleure sol
                    # print("new eval", new_eval)
                    # print("best voisin", best_voisin)
                    if new_eval < best_voisin:
                        # print("new eval< best voisin")
                        best_voisin = new_eval
                        best_voisin_sol = s
                        best_voisin_detail = new_detail
                        interdit = liste_interdit[v]
                        mac_best = mac

        # mise à jour permutations interdites, uniquement une fois best voisin trouvé
        listes_taboo[mac_best][interdit[0]][interdit[1]] = it + dureeTaboo

        current_makespan = best_voisin
        current_sol = best_voisin_sol
        current_detail = best_voisin_detail
        critiques, times = ge.chemin_critique(current_detail, n, m, machines, durations, current_sol)
        # print("current_makesan", current_makespan)

        # si solution courante est meilleure que meilleure solution, update meilleure sol ***
        if current_makespan < meilleure:
            meilleure = current_makespan
            best_sol = current_sol
            print("meilleure updated: ", meilleure)
            best_detail = current_detail
            val = ge.validate_detail(best_detail, durations, machines, n, m)
            print("val: ", val)

            # critiques, times = chemin_critique(best_detail, n, m, machines, durations, best_sol)

        # arret si time-out ou k>maxiter, on continue meme si pas d'amélioration
        # else: #best_voisin_eval >= meilleure:
        # ("no improvement")
        # break

    return meilleure, best_sol


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