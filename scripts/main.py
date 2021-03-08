import argparse
import os
import pandas as pd
import scripts.general as ge
import scripts.glouton as gl
from scripts.utils import compute_array_results, create_headers_df



def main():
    parser = argparse.ArgumentParser()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    print(ROOT_DIR)

    DATA_DIR = ROOT_DIR + "/../instances/"
    parser.add_argument('--instance', nargs='+', type=str, default="[abz5]")
    parser.add_argument('--gantt', help="Draw Gantt chart")
    parser.set_defaults(gantt=False)
    parser.add_argument('--descent', help="Add descent solver after 'gloutonne' methods")
    parser.set_defaults(descent=False)
    parser.add_argument('--taboo', help="Add taboo solver after 'gloutonne' methods")
    parser.set_defaults(taboo=False)
    parser.add_argument('--timeout',  type=int, default=60,
                        help="Parametrize the timeout for descend and taboo methods")
    parser.add_argument('--iter', type=int, default=100,
                        help="Parametrize the maximum number of iteration for the taboo method")
    parser.add_argument('--time_taboo', type=int, default=5,
                        help="Parametrize the number of iteration during the inverse permutation is forbidden for the "
                             "taboo method")
    args = parser.parse_args()

    for index, instance in enumerate(args.instance):
        filename = DATA_DIR + instance

        machines, durations, n, m = ge.generate_instance(filename, 4)  # we start at line 4 due to instance shape

        dict_gl = {
            "spt": gl.gloutonne_stp,
            "lrtp": gl.gloutonne_lrtp,
            "est_spt": gl.gloutonne_est_spt,
            "est_lrpt": gl.gloutonne_est_lrtp
        }

        results = compute_array_results(dict_gl, machines, durations, n, m,
                                        args.gantt, args.descent, args.taboo, args.timeout, args.iter, args.time_taboo)

        if index == 0:
            arrays = create_headers_df(args.descent, args.taboo)
            df_results = pd.DataFrame([j for sub in results for j in sub], index=arrays, columns=[instance])
        else:
            df_results.insert(index, instance, [j for sub in results for j in sub], allow_duplicates=True)

    df = df_results.sort_index(level=0).T
    df = df.round(1)

    # for i in list(df.columns.levels[0]):
    #     df[i]["Makespan"] = df[i]["Makespan"].astype('int64')
    #     print(df[i]["Makespan"])

    print(df)


if __name__ == '__main__':
    main()

