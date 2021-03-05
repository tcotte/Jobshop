"""
    Module descent_solver.py
    Module permettant d'implémenter un solver par métohde de descente
"""
import time

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
