import argparse
import sys

import numpy as np
import os
import pandas as pd
import math

infini = math.inf
import scripts.general as ge
import scripts.glouton as gl
import scripts.solvers.descent_solver as ds


def main():
    parser = argparse.ArgumentParser()
    ROOT_DIR = "C:/Users/User/Documents/Valdom/Jobshop"

    DATA_DIR = ROOT_DIR + "/instances/"
    parser.add_argument('--instance', type=str, default="abz5")
    args = parser.parse_args()

    filename = DATA_DIR + args.instance

    machines, durations, n, m = ge.generate_instance(filename, 4)  # we start at line 4 due to instance shape

    list_job, ressource = ge.init_sol_resources_nocycle(n, m,
                                                        machines)  # initialisation random mais sans cycle (baséee sur repre job)

    detail = ge.ressource_to_detaillee(ressource, n, m, durations, machines)
    # print(detail)

    makespan = ge.evaluate_detail(detail, n, m, durations)
    print("random sol makespan: ", makespan)

    val = ge.validate_detail(detail, durations, machines, n, m)
    # print(val)

    ressource2, all_mach_times = ge.detail_to_ressource(detail, durations, machines, n, m)

    # TODO chemin critique

    # HEURISTIQUES GLOUTONNES
    # Imlémentez les heuristiques STP et LRPT pour construire une solution représentée par ResourceOrder

    ### STP ###
    list_job_stp, ressource_stp = gl.goutonne_stp(machines, durations, n, m)

    ge.display_detailed_ressource(ressource_stp)

    detail_stp = ge.ressource_to_detaillee(ressource_stp, n, m, durations, machines)

    print("DETAIL" + str(detail_stp))
    print("stp: ", ge.evaluate_detail(detail_stp, n, m, durations))
    makespan_stp = ge.evaluate_detail(detail_stp, n, m, durations)
    path = ge.critical_path(n, m, durations, detail_stp, makespan_stp)
    # ge.draw_gantt(n, m, machines, durations, detail_stp)
    print("CRITICAL PATH ",path)
    # print(detail_stp)

    # blocks = ge.blocks_of_critical_path(machines, path)
    # print("BLOCKS --> " + str(blocks))

    # ressource_swapped = ge.swap(3, ressource_stp, 1,2)
    # ge.display_detailed_ressource(ressource_swapped)
    # for block in blocks:
    #     print(len(block))
    # print(len(blocks))
    # # ge.neighbors([['Job 2 /op 8', 2, 8, 45, 1926, 1971, 9], ['Job 5 /op 5', 5, 5, 72, 1971, 2043, 9], ['Job 3 /op 2', 5, 5, 72, 1971, 2043, 9]])
    # # blocks = [['Job 2 /op 8', 2, 8, 45, 1926, 1971, 9], ['Job 5 /op 5', 5, 5, 72, 1971, 2043, 9], ['Job 3 /op 2', 5, 5, 72, 1971, 2043, 9]]
    # block = ge.neighbors(blocks, 0)
    # print(ge.apply_on(ressource_stp, machines, block))

    ds.descent_solver(n, m, durations, ressource_stp, path, machines)

    ### LRTP ###
    # list_job_lrtp, ressource_lrtp = gl.goutonne_lrtp(machines, durations, n, m)
    # detail_lrtp = ge.ressource_to_detaillee(ressource_lrtp, n, m, durations, machines)
    # print("lrtp: ", ge.evaluate_detail(detail_lrtp, n, m, machines, durations))
    #
    # # Améliorez ces heuristiques : EST-SPT et EST-LRPT
    # # Evaluez ces heuristiques sur les instances ft et la
    #
    # ### EST STP ###
    # list_job_est_stp, ressource_est_stp = gl.gloutonne_est_spt(machines, durations, n, m)
    # detail_est_stp = ge.ressource_to_detaillee(ressource_est_stp, n, m, durations, machines)
    # print("est stp: ", ge.evaluate_detail(detail_est_stp, n, m, machines, durations))
    #
    # ### EST LRTP ###
    # list_job_est_lrtp, ressource_est_lrtp = gl.gloutonne_est_lrtp(machines, durations, n, m)
    # detail_est_lrtp = ge.ressource_to_detaillee(ressource_est_lrtp, n, m, durations, machines)
    # print("est lrtp: ", ge.evaluate_detail(detail_est_lrtp, n, m, machines, durations))


if __name__ == '__main__':
    main()

# METHODES DE DESCENTES
