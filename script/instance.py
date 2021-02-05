import numpy as np


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
    nb_machines = array[0][1] # number of machines

    return [nb_machines, nb_jobs, machines, durations]
