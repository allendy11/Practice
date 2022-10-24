'''
Created on Oct 24, 2022

@author: root
'''
from time import time
import pandas as pd
import numpy as np
import multiprocessing as mp
import os
from joblib import delayed, Parallel
from preprocess.create_taxa_meta import create_taxa_meta, set_remote_size, download_taxa_data


def meta_data_process(taxa, n_procs, is_purge):
    output_path = f"/home/neuroears/data_mount/study/data/NCBI_DHDH/{taxa}/assembly_summary.txt"
    df = create_taxa_meta(output_path, taxa, is_purge=False)
    dfs = np.array_split(df, n_procs*10)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(set_remote_size)(output_path, p_df, taxa, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)
    
    return gathered_df

def taxa_data_process():
    pass


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    taxa_list = ["fungi"]
    is_purge = True
    n_procs = mp.cpu_count() # 8 
    
    for taxa in taxa_list:
        print(f"[{taxa}]")
        t1 = time()
        df = meta_data_process(taxa, n_procs, is_purge)
        t2 = time()
        # print(df.head(1))
        print(f"{t2-t1:.3f} sec")
        
        # df_ = df[~df["is_downloaded"]]
        
        # t3 = time()
        # taxa_data_process
        # t4 = time()
        #
        # print(f"{t4-t1:.3f} sec")
        
        # print(df.head(1))
        break