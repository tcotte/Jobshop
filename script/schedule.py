# Argument
import argparse
import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
from plotly.figure_factory import create_gantt

parser = argparse.ArgumentParser()
DATA_DIR = "instances/"
parser.add_argument('--instance', type=str, default=DATA_DIR + "aaa1")
args = parser.parse_args()


def compute_data(instance):
    f = open(instance, "r")
    content = f.read()
    f.close()

    lines = content.split("\n")
    array = []

    for line in lines:
        if line.startswith('#'):  # filter lines of comment
            pass
        else:
            numbers = line.split(" ")
            while numbers.count('') > 0:
                numbers.remove('')
            for j in range(len(numbers)):
                numbers[j] = int(numbers[j])

            if numbers != []:
                array.append(numbers)

    machines = np.matrix(array[1:])[:, ::2]
    durations = np.matrix(array[1:])[:, 1::2]
    nb_jobs = array[0][0]  # number of jobs
    nb_machines = array[0][1]

    return [nb_machines, nb_jobs, machines, durations]


def get_naive_makespan(durations):
    return np.sum(durations)


def random_solution(nb_machines, nb_jobs, machines):
    list_solution = []
    list_job_operation = []

    for n in range(nb_machines):
        list_ressource = np.random.permutation(np.arange(1, nb_jobs + 1)).tolist()
        list_solution.append(list_ressource)

    for i in range(len(list_solution)):
        list_tuples = []
        for j in range(nb_jobs):
            job_number = list_solution[i][j]
            operation = machines[job_number - 1, i] + 1
            # append tuple2<Integer, Integer> with job and operation
            list_tuples.append((job_number, operation))
        list_job_operation.append(list_tuples)

    return list_job_operation


def df_ordered_repr(list_job_operation, nb_machines):
    list_ressources = []
    [list_ressources.append("r" + str(i + 1)) for i in range(nb_machines)]
    return pd.DataFrame(list_job_operation, index=list_ressources)


def index_col(t, df):
    col = df.columns[df.isin([t]).any()].tolist()[0]
    str_index = df.index[df[col].isin([t])].tolist()[0]
    index = str_index.replace("r", "")
    index = int(index)
    return str_index, index - 1, col


def detailed_repr(nb_jobs, nb_machines, df_solution, durations):
    repr_job = np.zeros((nb_jobs, nb_machines))
    counter_job = np.zeros(nb_jobs)
    counter_ress = np.zeros(nb_machines)
    ready_job = np.zeros(nb_jobs)
    ready_ress = np.zeros(nb_machines)

    while any(x != nb_jobs for x in counter_ress):
        for job in range(1, nb_jobs + 1):
            for op in range(1, nb_machines + 1):
                t = (job, op)
                ind, ressource, col = index_col(t, df_solution)

                if (col == counter_ress[ressource]) & (op - 1 == counter_job[job - 1]):
                    repr_job[job - 1][op - 1] = max(ready_job[job - 1], ready_ress[ressource])

                    ready_ress[ressource] = ready_ress[ressource] + durations[job - 1, op - 1] + ready_job[job - 1]
                    ready_job[job - 1] = repr_job[job - 1][op - 1] + + durations[job - 1, op - 1]

                    counter_ress[ressource] += 1
                    counter_job[job - 1] += 1

    return repr_job


def df_detailed_repr(nb_jobs, detailed_repr):
    list_jobs = []
    [list_jobs.append('J' + str(x)) for x in range(1, nb_jobs + 1)]
    df_repr_detail = pd.DataFrame(data=detailed_repr, index=list_jobs, columns=range(1, 4))
    return df_repr_detail


def draw_gantt(nb_jobs, nb_machines, machines, durations, representation):
    today = date.today()
    # print(detailed_repr[0][0])
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