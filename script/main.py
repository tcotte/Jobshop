import argparse
import numpy as np
from schedule import *


def main():
    parser = argparse.ArgumentParser()
    DATA_DIR = "instances/"
    parser.add_argument('--instance', type=str, default=DATA_DIR + "aaa1")
    args = parser.parse_args()

    nb_machines, nb_jobs, machines, durations = compute_data(args.instance)

    list_job_operation = random_solution(nb_machines, nb_jobs, machines)
    df = df_detailed_repr(list_job_operation, nb_machines)
    print(df)



if __name__ == '__main__':
    main()
