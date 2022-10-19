'''
Created on 19 Oct 2022

@author: root
'''

import os
import multiprocessing
import numpy as np
import pandas as pd
from joblib import delayed, Parallel
from preprocess.FTPConnection import FTPConnection
from preprocess.create_taxa_meta import download_summary, get_remote_size, get_remote_data
import time


def create_taxa_meta(taxa, n_procs, is_purge):
    summary_output_path = f"/Volumes/study/data/NCBI_DH/{taxa}/assembly_summary.txt"
    taxa_output_dir = f"/Volumes/study/data/NCBI/{taxa}"

    df = download_summary(summary_output_path, taxa, is_purge)

    dfs = np.array_split(df, n_procs)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(get_remote_size)(
        summary_output_path, p_df, taxa, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)

    return gathered_df, summary_output_path


def download_taxa_data(output_path, df, n_procs, is_purge):
    dfs = np.array_split(df, n_procs)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(get_remote_data)(
        output_path, p_df, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)
    # print(gathered_df.loc[:,"local_path": "is_downloaded"])
    return gathered_df


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    taxa_list = ["viral", "protozoa", "bacteria"]
    n_procs = multiprocessing.cpu_count()
    is_purge = False

    for taxa in taxa_list:
        start = time.time()
        try:
            df, output_path = create_taxa_meta(taxa, n_procs, is_purge)

            view = df[~df["is_downloaded"]]
            df = download_taxa_data(output_path, view, n_procs, is_purge)

            # print(df.loc[:,["local_size", "remote_size", "is_downloaded"]])
            print(len(df[~df["is_downloaded"]]))
        except:
            end = time.time()
            print(f"{end-start:.3f} sec")

        end = time.time()
        print(f"{end-start:.3f} sec")

        break
