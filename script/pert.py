import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def pert_df(nb_jobs, nb_machines, task_with_machine, start_time, durations):
    durations = durations.tolist()
    task_with_machine = task_with_machine.tolist()

    list_tasks = []
    for i in range(nb_jobs):
        list_dependency = []
        task_name = None
        for j in range(nb_machines):
            if task_name is not None:
                list_dependency.append(task_name)

            task_name = "Job " + str(i + 1) + " / op " + str(j + 1)

            if j == 0:
                dependency = "Start"
            else:
                dependency = "Job " + str(i + 1) + " / op " + str(j)

            list_tasks.append([task_name, dependency, str("r" + str(task_with_machine[i][j] + 1))])

        list_tasks.append(["End", "Job 2 / op " + str(j + 1), "r3"])
        list_tasks.append(["End", "Job 1 / op " + str(j + 1), "r3"])
    df = pd.DataFrame({'from': [row[0] for row in list_tasks], 'to': [row[1] for row in list_tasks]})
    carac = pd.DataFrame({'ID': [row[0] for row in list_tasks], 'ressource': [row[2] for row in list_tasks]})

    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())

    plt.show()
