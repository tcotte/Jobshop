from script.schedule import index_col
import numpy as np


# def spt(nb_jobs, nb_machines, machines, durations, df_resource_order):
#     job_counter = np.zeros(nb_jobs)
#     counter_ress = np.zeros(nb_machines)
#     # list_solutions = np.zeros((nb_machines, nb_jobs))
#     sorted_op = sort_by_duration(nb_jobs, machines, durations)
#     print("sorted operation " + str(sorted_op))
#     list_solutions = [[0 for x in range(nb_jobs)] for y in range(nb_machines)]
#     print("list_solutions " + str(list_solutions))
#
#     for op in range(1, nb_machines + 1):
#         todo_list = []
#         ressource_list = []
#         for job in range(1, nb_jobs + 1):
#             if op == 1:
#                 t = (job, op)
#                 _, ressource, _ = index_col(t, df_resource_order)
#                 job_counter[job - 1] += 1
#
#             else:
#                 t = (job, sorted_op[job - 1][op - 2] + 1)
#                 # sorted_op[job - 1].pop(0)
#                 if t[1] == job_counter[job - 1] + 1:
#                     todo_list.append(t)
#                     job_counter[job - 1] += 1
#                     _, ressource, _ = index_col(t, df_resource_order)
#                 else:
#                     print("Not realisable job "+str(job+1)+"/"+str(sorted_op[job - 1][op - 2]+1))
#                     sorted_op[job - 1].append(t[1])
#                     pass
#
#             print(str(t) + str(ressource))
#             ressource_list.append(ressource)
#
#         for ind, val in enumerate(todo_list):
#             ressource = ressource_list[ind]
#             print("ressource = " + str(ressource))
#             print("coutner_ress = " + str(counter_ress[ressource]))
#             list_solutions[ressource][int(counter_ress[ressource])] = val
#             # list_solutions[ressource][int(counter_ress[ressource])] = 1
#             counter_ress[ressource] += 1
#
#             print(list_solutions)
#
#     print(job_counter)


def spt(nb_jobs, nb_machines, machines, durations, df_resource_order):
    job_counter = np.zeros(nb_jobs)
    counter_ress = np.zeros(nb_machines)
    list_realisable = [0 for x in range(nb_jobs)]
    shortest_task = 0
    durations = durations.tolist()
    periods = [0 for x in range(nb_jobs)]
    list_solutions = [[0 for x in range(nb_jobs)] for y in range(nb_machines)]
    machines = machines.tolist()
    op = 0

    while any(x != nb_jobs + 1 for x in job_counter):
        if op == 0:
            for job in range(nb_jobs):
                t = (job, op)
                list_realisable[job] = t
                # print(list_realisable)

        # print(list_realisable)
        for ind, val in enumerate(list_realisable):
            periods[ind] = durations[val[0]][val[1]]

        shortest_task = list_realisable[np.argmin(periods)]
        _, ressource, _ = index_col((shortest_task[0] + 1, shortest_task[1] + 1), df_resource_order)
        list_solutions[ressource][int(counter_ress[ressource])] = shortest_task
        counter_ress[ressource] += 1

        list_realisable.pop(np.argmin(periods))

        if shortest_task[1] + 1 < nb_machines:
            list_realisable.insert(shortest_task[0], (shortest_task[0], shortest_task[1] + 1))
        job_counter[shortest_task[0]] += 1
        op += 1

        print(job_counter)
        print(list_realisable)
    print(list_solutions)

    a = []
    for i in list_solutions:
        a.append([(x + 1, y + 1) for x, y in i])

    return a


def sort_by_duration(nb_jobs, machines, durations):
    durations = durations.tolist()
    machines = machines.tolist()
    tasks = []
    periods = []
    tasks_ordered = []
    for job in range(nb_jobs):
        tasks = machines[job]
        periods = durations[job]
        tasks_periods = list(zip(tasks, periods))
        tasks_periods_filtered = [(x, y) for x, y in tasks_periods if x != 0]  # delete first operation
        tasks_periods_filtered.sort(key=sort_second)

        tasks_ordered.append([x for x, y in tasks_periods_filtered])
    return tasks_ordered


def sort_second(val):
    return val[1]
