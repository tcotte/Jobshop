import argparse
import os
import sys
import numpy as np

from script.instance import compute_data
from script.pert import pert_df
from script.schedule import df_ordered_repr, random_solution, detailed_repr, df_detailed_repr, draw_gantt, \
    isValid, compute_makespan, critical_path
from script.solvers import spt, lrpt


def main():
    parser = argparse.ArgumentParser()
    ROOT_DIR = sys.path[1]
    DATA_DIR = ROOT_DIR + "/instances/"
    parser.add_argument('--instance', type=str, default="aaa1")
    args = parser.parse_args()

    nb_machines, nb_jobs, machines, durations = compute_data(DATA_DIR + args.instance)

    # list_job_operation = random_solution(nb_machines, nb_jobs, machines)
    # # Create solution which works
    # # list_job_operation = [[(1, 1), (2, 2)], [(2, 1), (1, 2)], [(1, 3), (2, 3)]]
    # # list_job_operation = [[(2, 2), (1, 1)], [(2, 1), (1, 2)], [(1, 3), (2, 3)]]
    # df_solution = df_ordered_repr(list_job_operation, nb_machines)
    # print("Resource order representation")
    # print(df_solution)
    #
    # start_time = detailed_repr(nb_jobs, nb_machines, df_solution, durations)
    # df_repr = df_detailed_repr(nb_jobs, start_time)
    # print("\n Detailed representation")
    # print(df_repr)
    #
    # valid = isValid(nb_jobs, nb_machines, durations, machines, start_time)
    # print("\n Solution valid ? " + str(valid))
    #
    # makespan = compute_makespan(nb_jobs, nb_machines, durations, start_time)
    # print("makespan --> " + str(makespan))
    # # draw_gantt(nb_jobs, nb_machines, machines, durations, start_time)
    #
    # pert_df(nb_jobs, nb_machines, machines, start_time, durations)
    # print("critical path --> " + str(critical_path(nb_jobs, nb_machines, durations, start_time, makespan)))

    print("############### Solve ###############")
    solution = spt(nb_jobs, nb_machines, machines, durations)
    print(solution)
    df_solution = df_ordered_repr(solution, nb_machines)
    print(df_solution)
    start_time = detailed_repr(nb_jobs, nb_machines, df_solution, durations)
    df_repr = df_detailed_repr(nb_jobs, start_time)
    valid = isValid(nb_jobs, nb_machines, durations, machines, start_time)
    print("\n Solution valid ? " + str(valid))
    draw_gantt(nb_jobs, nb_machines, machines, durations, start_time)


if __name__ == '__main__':
    main()
