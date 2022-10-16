'''
Created on 14 Oct 2022

@author: allen
'''

import multiprocessing
import numpy as np
import pandas as pd
from joblib import delayed, Parallel
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
        result_dfs = Parallel(n_jobs=n_procs)(delayed(download_taxa_data)(
            p_df, taxa, p_id) for p_id, p_df in enumerate(dfs))
        gathered_df = pd.concat(result_dfs, axis=0)
