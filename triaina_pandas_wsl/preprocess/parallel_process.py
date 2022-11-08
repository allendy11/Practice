'''
Created on Oct 18, 2022

@author: root
'''

import os, multiprocessing
import numpy as np
import pandas as pd
from joblib import delayed, Parallel
from preprocess.FTPConnection import FTPConnection
from preprocess.create_taxa_meta import download_summary, get_remote_size, get_remote_data


def create_taxa_meta(taxa, n_procs, is_purge):
    summary_output_path = f"/home/neuroears/data_mount/study/data/NCBI_DHDH/{taxa}/assembly_summary.txt"
    taxa_output_dir = f"/home/neuroears/data_mount/study/data/NCBI/{taxa}"
    
    
    df = download_summary(summary_output_path, taxa, is_purge=False)

    dfs = np.array_split(df, n_procs)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(get_remote_size)(summary_output_path, p_df, taxa, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)
    # print(gathered_df.loc[:,["remote_size","is_downloaded"]])
    # print(len(df), len(gathered_df))
    return gathered_df, summary_output_path
    
    

def download_taxa_data(output_path, df, n_procs, is_purge):
    dfs = np.array_split(df, n_procs)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(get_remote_data)(output_path, p_df, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)
    # print(gathered_df.loc[:,"local_path": "is_downloaded"])
    return gathered_df
    


if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa" ,"bacteria"]
    n_procs = multiprocessing.cpu_count()
    is_purge = False
    
    for taxa in taxa_list:
        df, output_path = create_taxa_meta(taxa, n_procs, is_purge)
        
        df = download_taxa_data(output_path, df, n_procs, is_purge)
        # print(df.loc[:,["local_size", "remote_size", "is_downloaded"]])
        
        print(len(df[df["is_downloaded"] == False]))
        break
        
        