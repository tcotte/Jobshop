"""
    Module descent_solver.py
    Module permettant d'implémenter un solver par métohde de descente
"""

import numpy as np
import scripts.general as ge
import math
import matplotlib.pyplot as plt


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
        job = i[1]
        op = i[2]
        # i = i.pop([3,4,5])
        i.append(get_ressource(machines, job, op))

    blocks = []
    i = 0
    memory = []

    while i < len(critical_path) - 1:
        current_task = critical_path[i]
        next_task = critical_path[i + 1]

        if current_task[6] == next_task[6]:
            memory.append(current_task)

        else:
            if len(memory) != 0:
                memory.append(current_task)
                blocks.append(memory)
                memory = []

        i += 1

    print("BLOCKS" + str(blocks))

    return transform_blocks(blocks)


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
    :return: nouvelle solution généré à l'aidedu bloc de voisinage
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


def descent_solver(n, m, durations, init_sol, path, machines, early_stop=30):
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
    solution = init_sol

    ge.display_detailed_ressource(solution)

    detail_init = ge.ressource_to_detaillee(solution, n, m, durations, machines)
    makespan = ge.evaluate_detail(detail_init, n, m, durations)

    list_makespan = [makespan]

    while counter < early_stop:
        block = neighbors(blocks, np.random.randint(low=0, high=interval))
        print("BLOCK ", block)
        solution = apply_on(n, m, solution, machines, durations, block)

        detail = ge.ressource_to_detaillee(solution, n, m, durations, machines)

        if ge.evaluate_detail(detail, n, m, durations) < makespan:

            makespan = ge.evaluate_detail(detail, n, m, durations)


            ge.display_detailed_ressource(solution)
            counter = 0
        else:
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
