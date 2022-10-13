'''
Created on Oct 12, 2022

@author: root
'''

import os
import pandas as pd
import multiprocessing
import numpy as np
from joblib import delayed, Parallel
from preprocess.FTPConnection import FTPConnection
from preprocess.create_taxa_meta import create_taxa_meta
from preprocess.create_taxa_meta import modify_taxa_meta
from preprocess.create_taxa_meta import download_taxa_data


    

if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    n_procs = multiprocessing.cpu_count()
    
    
    for taxa in taxa_list:
        df = create_taxa_meta(taxa)
        df = modify_taxa_meta(df, taxa)
        dfs = np.array_split(df, n_procs)
        result_dfs = Parallel(n_jobs=n_procs)(delayed(download_taxa_data)(p_df, p_id) for p_id, p_df in enumerate(dfs))
        gathered_df = pd.concat(result_dfs, axis=0)
        
        break