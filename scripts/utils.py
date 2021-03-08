import numpy as np
import math
import time
import scripts.general as ge
import scripts.solvers.descent_solver as ds


def add_gap(results):
    makespan_minimum = math.inf
    for list_results in results:
        if list_results[1] < makespan_minimum:
            makespan_minimum = list_results[1]

    for list_results in results:
        list_results.append((list_results[1] / makespan_minimum - 1) * 100)
    return results


def compute_array_results(dict_methods, machines, durations, n, m, gantt, descent, taboo, timeout, max_iter, time_taboo):
    results = []
    for name, function in dict_methods.items():
        # starting time
        start = time.time()

        list_job, ressource = function(machines, durations, n, m)
        detail = ge.ressource_to_detaillee(ressource, n, m, durations, machines)
        makespan = ge.evaluate_detail(detail, n, m, durations)

        # end time
        end = time.time()
        if gantt: ge.draw_gantt(n, m, machines, durations, detail)
        results.append([end - start, makespan])

        if descent:
            start = time.time()
            makespan, _ = ds.descent_solver(machines, durations, n, m, ressource, timeout)
            end = time.time()
            results.append([end - start, makespan])

        if taboo:
            start = time.time()
            makespan, _ = ds.taboo_solver(machines, durations, n, m, timeout, time_taboo, max_iter)
            end = time.time()
            results.append([end - start, makespan])

    return add_gap(results)


def arrays_for_headers(list_method):
    list_params = ["Temps (s)", "Makespan", "Ecart"]
    arr = []
    params = []

    for i in list_method:
        arr += 3 * [i]
        params += list_params

    headers = [
        np.array(arr),
        np.array(params),
    ]
    return headers


def create_headers_df(descent, taboo):
    if not descent and not taboo:
        arr = ["spt", "spt", "spt", "lrtp", "lrtp", "lrtp", "est_spt", "est_spt", "est_spt", "est_lrtp",
               "est_lrtp", "est_lrtp"]
        params = ["Temps (s)", "Makespan", "Ecart", "Temps (s)", "Makespan", "Ecart", "Temps (s)", "Makespan",
                  "Ecart", "Temps (s)", "Makespan", "Ecart"]
        arrays = [np.array(arr), np.array(params)]

    elif descent and not taboo:
        list_method = ["spt", "descent_spt", "lrtp", "descent_lrtp", "est_spt", "descent_est_spt", "est_lrtp",
                       "descent_est_lrpt"]

        arrays = arrays_for_headers(list_method)

    elif descent and taboo:
        list_method = ["spt", "descent_spt", "taboo_spt", "lrtp", "descent_lrtp", "taboo_lrpt", "est_spt",
                       "descent_est_spt",
                       "taboo_est_spt", "est_lrtp", "descent_est_lrpt", "taboo_est_lrpt"]

        arrays = arrays_for_headers(list_method)

    else:
        list_method = ["spt", "taboo_spt", "lrtp", "taboo_lrpt", "est_spt", "taboo_est_spt", "est_lrtp",
                       "taboo_est_lrpt"]
        arrays = arrays_for_headers(list_method)

    return arrays