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
    n_procs = multiprocessing.cpu_count()
    is_purge = True
    for taxa in taxa_list:
        df, output_path = download_summary(taxa, is_purge)
        df = modify_taxa_meta(df, taxa)
        dfs_1 = np.array_split(df, n_procs)

        start = time.time()

        result_dfs_1 = Parallel(n_jobs=n_procs)(delayed(check_is_downloaded)(
            output_path, p_df, taxa, p_id, is_purge=is_purge) for p_id, p_df in enumerate(dfs_1))
        gathered_df = pd.concat(result_dfs_1, axis=0)

        gathered_df = gathered_df[~gathered_df["is_downloaded"]]
        print(gathered_df.head(1))

        dfs_2 = np.array_split(gathered_df, n_procs)
        result_dfs_2 = Parallel(n_jobs=n_procs)(delayed(download_taxa_data)(
            p_df, taxa, p_id) for p_id, p_df in enumerate(dfs_2))
        gathered_df_2 = pd.concat(result_dfs_2, axis=0)

        end = time.time()

        print(f"total downloaded: {len(gathered_df)}")
        print(f"{end-start:.3f} sec")
