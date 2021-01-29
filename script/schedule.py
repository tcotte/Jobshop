# Argument
import argparse
import numpy as np
import pandas as pd
from numpy.random import default_rng


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
        rng = default_rng()
        list_ressource = rng.choice((1, nb_jobs), size=nb_jobs, replace=False).tolist()
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


def df_detailed_repr(list_job_operation, nb_machines):
    list_ressources = []
    [list_ressources.append("r" + str(i + 1)) for i in range(nb_machines)]
    return pd.DataFrame(list_job_operation, index=list_ressources)

