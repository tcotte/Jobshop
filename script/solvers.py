from script.schedule import index_col
import numpy as np


def spt(nb_jobs, nb_machines, machines, durations):
    job_counter = [0 for x in range(nb_jobs)]
    counter_ress = np.zeros(nb_machines)
    list_realisable = [0 for x in range(nb_jobs)]
    shortest_task = 0
    durations = durations.tolist()
    periods = [0 for x in range(nb_jobs)]
    list_solutions = [[0 for x in range(nb_jobs)] for y in range(nb_machines)]
    machines = machines.tolist()
    op = 0

    while any(x != nb_jobs for x in job_counter):
    # while job_counter:
        if op == 0:
            for job in range(nb_jobs):
                t = (job, op)
                list_realisable[job] = t

        for ind, val in enumerate(list_realisable):
            if val[1] == "/":
                periods[ind] = float("inf")
            else:
                periods[ind] = durations[val[0]][val[1]]

        shortest_task = list_realisable[np.argmin(periods)]
        # _, ressource, _ = index_col((shortest_task[0] + 1, shortest_task[1] + 1), df_resource_order)
        ressource = machines[shortest_task[0]][shortest_task[1]]
        list_solutions[ressource][int(counter_ress[ressource])] = shortest_task
        counter_ress[ressource] += 1
        print("argmin " + str(periods))
        list_realisable.pop(np.argmin(periods))

        if shortest_task[1] + 1 < nb_machines:
            list_realisable.insert(shortest_task[0], (shortest_task[0], shortest_task[1] + 1))
        else:
            list_realisable.insert(shortest_task[0], (shortest_task[0], "/"))

        job_counter[shortest_task[0]] += 1
        op += 1

        print(job_counter)
        print(list_realisable)
    print(list_solutions)

    a = []
    for i in list_solutions:
        a.append([(x + 1, y + 1) for x, y in i])

    return a


def lrpt(nb_jobs, nb_machines, machines, durations):
    durations = durations.tolist()
    machines = machines.tolist()
    remaining_time = list(np.sum(durations, axis=1))

    job_counter = np.zeros(nb_jobs)
    counter_ress = np.zeros(nb_machines)
    list_realisable = [0 for x in range(nb_jobs)]

    list_solutions = [[0 for x in range(nb_jobs)] for y in range(nb_machines)]
    op = 0

    while list_realisable:
        if op == 0:
            for job in range(nb_jobs):
                t = (job, op)
                list_realisable[job] = t

        print("remaining_time --> " + str(remaining_time))
        print("list realisable --> " + str(list_realisable))
        task_todo = list_realisable[np.argmax(remaining_time)]

        list_realisable.pop(np.argmax(remaining_time))
        remaining_time[np.argmax(remaining_time)] -= durations[task_todo[0]][task_todo[1]]
        if 0 in remaining_time: remaining_time.remove(0)

        # _, ressource, _ = index_col((task_todo[0] + 1, task_todo[1] + 1), df_resource_order)
        ressource = machines[task_todo[0]][task_todo[1]]
        list_solutions[ressource][int(counter_ress[ressource])] = task_todo
        counter_ress[ressource] += 1

        if task_todo[1] + 1 < nb_machines:
            list_realisable.insert(task_todo[0], (task_todo[0], task_todo[1] + 1))
        job_counter[task_todo[0]] += 1
        op += 1

    a = []
    for i in list_solutions:
        a.append([(x + 1, y + 1) for x, y in i])

    return a

# def sort_by_duration(nb_jobs, machines, durations):
#     durations = durations.tolist()
#     machines = machines.tolist()
#     tasks = []
#     periods = []
#     tasks_ordered = []
#     for job in range(nb_jobs):
#         tasks = machines[job]
#         periods = durations[job]
#         tasks_periods = list(zip(tasks, periods))
#         tasks_periods_filtered = [(x, y) for x, y in tasks_periods if x != 0]  # delete first operation
#         tasks_periods_filtered.sort(key=sort_second)
#
#         tasks_ordered.append([x for x, y in tasks_periods_filtered])
#     return tasks_ordered
#
#
# def sort_second(val):
#     return val[1]
