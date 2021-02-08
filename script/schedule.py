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
    # df_repr_detail = pd.DataFrame(data=detailed_repr, index=list_jobs, columns=range(1, 4))
    df_repr_detail = pd.DataFrame(data=detailed_repr, index=list_jobs)
    return df_repr_detail


def draw_gantt(nb_jobs, nb_machines, machines, durations, representation):
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


# Returns true if this schedule is valid (no constraint is violated) */
def isValid(nb_jobs, nb_machines, durations, task_with_machine, start_time):
    durations = durations.tolist()
    task_with_machine = task_with_machine.tolist()

    # Overlapping tasks on job issues
    for j in range(nb_jobs):
        for t in range(1, nb_machines):
            if start_time[j][t - 1] + durations[j][t - 1] > start_time[j][t]:
                return False

        # A job can't start before date 0
        for t in range(nb_machines):
            if start_time[j][t] < 0:
                return False

    # Overlapping machines issues
    for machine in range(nb_machines):
        for j1 in range(nb_jobs):
            t1 = task_with_machine[j1][machine]
            for j2 in range(j1 + 1, nb_jobs):
                t2 = task_with_machine[j2][machine]

                t1_first = start_time[j1][t1] + durations[j1][t1] <= start_time[j2][t2]
                t2_first = start_time[j2][t2] + durations[j2][t2] <= start_time[j1][t1]

                if not (t1_first or t2_first):
                    return False

    return True


def compute_makespan(nb_jobs, nb_machines, durations, start_time):
    makespan = -1
    durations = durations.tolist()
    for j in range(nb_jobs):
        makespan = np.maximum(makespan, int(start_time[j][nb_machines - 1] + durations[j][nb_machines - 1]))
    return makespan


def end_time(start_time, duration):
    return start_time + duration


def critical_path(nb_jobs, nb_machines, durations, start_time, makespan):
    critical_tasks = []
    end_list = []
    durations = durations.tolist()

    for i in range(nb_jobs):
        for j in range(nb_machines):
            end_list.append(
                ["Job " + str(i + 1) + " /op " + str(j + 1), durations[i][j], end_time(start_time[i][j], durations[i][j])])

    endTime = int(makespan)
    while endTime != 0:

        for task in end_list:
            if task[2] == endTime:
                critical_tasks.append(task[0])
                endTime -= task[1]
                pass # Avoid double tasks in the critical path (two tasks which finish in the same time)

    return critical_tasks
