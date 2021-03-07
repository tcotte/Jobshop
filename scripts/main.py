import argparse
import sys

import numpy as np
import os
import pandas as pd
import math
import time
infini = math.inf
import scripts.general as ge
import scripts.glouton as gl
import scripts.solvers.descent_solver as ds
from itertools import chain


def main():
    parser = argparse.ArgumentParser()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(ROOT_DIR)

    DATA_DIR = ROOT_DIR + "/../instances/"
    parser.add_argument('--instance',  nargs='+', type=str, default="[abz5]")
    parser.add_argument('--gantt', help="Draw Gantt chart")
    parser.set_defaults(gantt=False)
    args = parser.parse_args()

    for index, instance in enumerate(args.instance):
        filename = DATA_DIR + instance

        machines, durations, n, m = ge.generate_instance(filename, 4)  # we start at line 4 due to instance shape

    # TODO chemin Ajouter le tabou

    # HEURISTIQUES GLOUTONNES
    # Imlémentez les heuristiques STP et LRPT pour construire une solution représentée par ResourceOrder

        dict_gl = {
            "stp" : gl.gloutonne_stp,
            "lrtp" : gl.gloutonne_lrtp,
            "est_stp" : gl.gloutonne_est_spt,
            "est_lrpt" : gl.gloutonne_est_lrtp
        }

        results = []

        for name, function in dict_gl.items():
            # starting time
            start = time.time()

            list_job, ressource = function(machines, durations, n, m)
            detail = ge.ressource_to_detaillee(ressource, n, m, durations, machines)
            makespan = ge.evaluate_detail(detail, n, m, durations)

            # end time
            end = time.time()
            if args.gantt: ge.draw_gantt(n, m, machines, durations, detail)
            results.append([end-start, makespan])

        makespan_minimum = math.inf
        for list_results in results:
            if list_results[1] < makespan_minimum:
                makespan_minimum = list_results[1]

        for list_results in results:
            list_results.append((list_results[1]/makespan_minimum-1)*100)

        if index == 0:
            arrays = [
                np.array(["stp", "stp", "stp", "lrtp", "lrtp", "lrtp", "est_stp", "est_stp", "est_stp", "est_lrtp", "est_lrtp", "est_lrtp"]),
                np.array(["Temps (s)", "Makespan", "Ecart", "Temps (s)", "Makespan", "Ecart", "Temps (s)", "Makespan", "Ecart", "Temps (s)", "Makespan", "Ecart"]),
                ]
            # df_results = pd.DataFrame(list(chain.from_iterable(results)),  columns=arrays)
            df_results = pd.DataFrame([j for sub in results for j in sub], index=arrays, columns=[instance])
        else:
            df_results.insert(index, instance, [j for sub in results for j in sub], allow_duplicates=False)

    print(df_results)

    ### EST LRTP ###
    # list_job_est_lrtp, ressource_est_lrtp = gl.gloutonne_est_lrtp(machines, durations, n, m)
    # detail_est_lrtp = ge.ressource_to_detaillee(ressource_est_lrtp, n, m, durations, machines)
    # makespan_lrtp = ge.evaluate_detail(detail_est_lrtp, n, m, durations)
    # print("est lrtp: ", makespan_lrtp)
    #
    # path = ge.critical_path(n, m, durations, detail_est_lrtp, makespan_lrtp, machines, ressource_est_lrtp)
    #
    # makespan, solution_descent = ds.descent_solver(machines, durations, n, m, ressource_est_lrtp)
    #
    # detail_descent = ge.ressource_to_detaillee(solution_descent, n, m, durations, machines)
    # ge.draw_gantt(n, m, machines, durations, detail_descent)
    #
    # print("MAKESPAN :", makespan)


if __name__ == '__main__':
    main()

# METHODES DE DESCENTES
