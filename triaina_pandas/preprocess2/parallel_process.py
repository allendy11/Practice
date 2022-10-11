'''
Created on Oct 11, 2022

@author: root
'''

import pandas as pd
import numpy as np
import multiprocessing
from joblib import delayed, Parallel
from preprocess2.FTPConnection import FTPConnection


def create_taxa_meta(p_id, p_df, taxa):
    host = "ftp.ncbi.nlm.nih.gov"
    output_path = "/home/allen/data_mount/study/data/NCBI"
    output_my_path = "/home/allen/data_mount/study/data/NCBI_DHDH"
    ftp_connection = FTPConnection(host, output_path, output_my_path)
    ftp_connection.connect()
    
    ftp_connection.download_assembly_summary(taxa)
    
    df = ftp_connection.create_taxa_meta(taxa)
    
    ftp_connection.close()
    
    tsv_path = f"{output_my_path}/{taxa}-{p_id}.tsv"
    df.to_csv(tsv_path, sep='\t', index=False)
    return df
    
    
if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    input_path = "/home/allen/data_mount/study/data/NCBI_DHDH"
    n_procs = multiprocessing.cpu_count()
    # print(n_procs)
    
    for taxa in taxa_list:
        input_summary_path = f"{input_path}/{taxa}/assembly_summary.txt"
        df = pd.read_csv(input_summary_path, sep='\t', skiprows=1)
        dfs = np.array_split(df, n_procs)
        result_dfs = Parallel(n_jobs=n_procs)(delayed(create_taxa_meta)(p_id, a_df, taxa) for p_id, a_df in enumerate(dfs))
        gathered_df = pd.concat(result_dfs, axis=0)
        break