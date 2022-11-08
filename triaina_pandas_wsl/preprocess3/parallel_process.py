'''
Created on Nov 1, 2022

@author: root
'''
from time import time
import pandas as pd
import numpy as np
import multiprocessing as mp
import os
from joblib import delayed, Parallel
from preprocess.create_taxa_meta import create_taxa_meta, create_meta_tsv, download_taxa_data


def get_size_process(taxa, n_procs, is_purge):
    output_path = f"/home/neuroears/data_mount/study/data/NCBI_DH/{taxa}/assembly_summary.txt"
    df = create_taxa_meta(output_path, taxa, is_purge=False)
    dfs = np.array_split(df, n_procs*100)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(create_meta_tsv)(output_path, p_df, taxa, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)
    
    return gathered_df

def get_file_process(df_, n_procs, is_purge):
    dfs = np.array_split(df, n_procs*100)
    result_dfs = Parallel(n_jobs=n_procs)(delayed(download_taxa_data)(p_df, taxa, p_id, is_purge) for p_id, p_df in enumerate(dfs))
    gathered_df = pd.concat(result_dfs, axis=0)
    
    return gathered_df

if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    os.environ["OMP_NUM_THREADS"] = "1"  # export OMP_NUM_THREADS=4
    os.environ["OPENBLAS_NUM_THREADS"] = "1"  # export OPENBLAS_NUM_THREADS=4
    os.environ["MKL_NUM_THREADS"] = "1"  # export MKL_NUM_THREADS=6
    # export VECLIB_MAXIMUM_THREADS=4
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"  # export NUMEXPR_NUM_THREADS=6
    
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    taxa_list = ["bacteria"]
    is_purge = False
    n_procs = mp.cpu_count() # 8 
    print(f"n_procs: {n_procs}")
    
    for taxa in taxa_list:
        print(f"taxa: {taxa}, is_purge: {is_purge}")
        t1 = time()
        df = get_size_process(taxa, n_procs, is_purge)
        t2 = time()
        print(f"{t2-t1:.3f} sec")
        
        t3 = time()
        df_ = df[df["is_downloaded"] == False]
        df = get_file_process(df_, n_procs, is_purge)
        t4 = time()
        print(f"{t4-t3:.3f} sec")
