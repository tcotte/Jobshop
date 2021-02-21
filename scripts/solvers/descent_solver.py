import numpy as np
import scripts.general as ge


def blocks_of_critical_path(machines, critical_path):
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
    for ind_bloc, bloc in enumerate(blocks):
        for ind_task, task in enumerate(bloc):
            blocks[ind_bloc][ind_task] = transform_to_tuples(task)

    return blocks


def transform_to_tuples(task):
    task_tuple = (task[1], task[2])
    return task_tuple


def get_ressource(machines, job, operation):
    return machines[job, operation]


#################################################

def swap(index, ressource, t1, t2):
    ressource[index][t1], ressource[index][t2] = ressource[index][t2], ressource[index][t1]
    return ressource[index]


def neighbors(blocks, index):
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


def apply_on(solution, machines, block):
    if len(block[0]) == 2:
        first_task = block[0]


    elif len(block[0]) > 2:
        block = block[np.random.randint(low=0, high=2)]  # get a random neighbor
        first_task = block[0]

    else:
        raise ValueError('A block can\'t be composed of one task')

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
    blocks = blocks_of_critical_path(machines, path)
    interval = len(blocks)
    print("BLOCKS --> " + str(blocks))

    counter = 0
    solution = init_sol

    ge.display_detailed_ressource(solution)

    detail_init = ge.ressource_to_detaillee(solution, n, m, durations, machines)
    makespan = ge.evaluate_detail(detail_init, n, m, durations)

    while counter < early_stop:
        block = neighbors(blocks, np.random.randint(low=0, high=interval))
        print("BLOCK ", block)
        solution = apply_on(solution, machines, block)
        detail = ge.ressource_to_detaillee(solution, n, m, durations, machines)

        if ge.evaluate_detail(detail, n, m, durations) < makespan:

            makespan = ge.evaluate_detail(detail, n, m, durations)
            print(makespan)
            ge.display_detailed_ressource(solution)
            counter = 0
        else:
            counter += 1

    return solution
