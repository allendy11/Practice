'''
Created on 14 Oct 2022

@author: allen
'''
import time
import multiprocessing
import numpy as np
import pandas as pd
from joblib import delayed, Parallel
from preprocess.create_taxa_meta import download_summary, modify_taxa_meta, check_is_downloaded, download_taxa_data

if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    taxa_list = ["fungi", "viral", "protozoa", "bacteria"]
    n_procs = multiprocessing.cpu_count()
    for taxa in taxa_list:
        df = download_summary(taxa)
        df = modify_taxa_meta(df, taxa)
        dfs_1 = np.array_split(df, n_procs)

        start = time.time()

        result_dfs = Parallel(n_jobs=n_procs)(delayed(check_is_downloaded)(
            p_df, taxa, p_id) for p_id, p_df in enumerate(dfs_1))
        gathered_df = pd.concat(result_dfs, axis=0)

        dfs_2 = np.array_split(gathered_df, n_procs)
        result_dfs_2 = Parallel(n_jobs=n_procs)(delayed(download_taxa_data)(
            p_df, taxa, p_id) for p_id, p_df in enumerate(dfs_2))
        gathered_df_2 = pd.concat(result_dfs_2, axis=0)

        end = time.time()

        print(f"total downloaded: {len(gathered_df)}")
        print(f"{end-start:.3f} sec")

        break
