import argparse
import os
import sys
import numpy as np

from script.schedule import df_ordered_repr, random_solution, compute_data, detailed_repr, df_detailed_repr, draw_gantt


def main():
    parser = argparse.ArgumentParser()
    ROOT_DIR = sys.path[1]
    DATA_DIR = ROOT_DIR + "/instances/"
    parser.add_argument('--instance', type=str, default="aaa1")
    args = parser.parse_args()

    nb_machines, nb_jobs, machines, durations = compute_data(DATA_DIR + args.instance)

    # list_job_operation = random_solution(nb_machines, nb_jobs, machines)
    # Create solution which works
    list_job_operation = [[(1, 1), (2, 2)], [(2, 1), (1, 2)], [(1, 3), (2, 3)]]
    df_solution = df_ordered_repr(list_job_operation, nb_machines)
    print(df_solution)

    representation = detailed_repr(nb_jobs, nb_machines, df_solution, durations)
    print(representation)
    df_repr = df_detailed_repr(nb_jobs, representation)
    print(df_repr)

    draw_gantt(nb_jobs, nb_machines, machines, durations, representation)


if __name__ == '__main__':
    main()
