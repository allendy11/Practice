'''
Created on Nov 14, 2022

@author: root
'''
import os
import pandas as pd
import numpy as np
import multiprocessing as mp
from joblib import delayed, Parallel
from preprocess.FTPConnection import FTPConnection
from tqdm import tqdm
from time import time

def set_local_path(ftp_path, taxa):
    local_dir = f"/home/neuroears/data_mount/study/data/NCBI/{taxa}"
    
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    file_name = os.path.basename(ftp_path)
    local_path = f"{local_dir}/{file_name}_genomic.fna.gz"
    
    return local_path

def modify_taxa_meta(output_path, taxa):
    df = pd.read_csv(output_path, sep='\t', skiprows=1, low_memory=False)
    df.rename(columns={"# assembly_accession": "assembly_accession"}, inplace=True)
    
    df = df[df["ftp_path"] != 'na'].copy()
    
    df["http_path"] = df["ftp_path"]
    df["ftp_path"] = df["ftp_path"].str.replace("http", "ftp")
    df["local_path"] = df["ftp_path"].map(lambda ftp_path: set_local_path(ftp_path, taxa))
    
    return df

def create_taxa_meta(taxa):
    output_path = f"/home/neuroears/data_mount/study/data/NCBI_DH/{taxa}/assembly_summary.txt"
    
    if os.path.exists(output_path):
        df = modify_taxa_meta(output_path, taxa)
        return df
    

def create_meta_tsv(taxa, p_id):
    tsv_path = f"/home/neuroears/data_mount/study/data/NCBI_DH/{taxa}/assembly_summary.txt.{p_id}"
    if os.path.exists(tsv_path):
        df = pd.read_csv(tsv_path, sep='\t')
        return df


def download_taxa_data(ftp_con, p_id, row, a_id):
    output_path = row[6]
    remote_path = row[7]
    remote_size = row[9]
    is_downloaded = row[10]
    
    # host = "ftp.ncbi.nlm.nih.gov"
    # ftp_con = FTPConnection()
    # ftp_con.set_host(host)
    ftp_con.connect()
    
    if remote_size == -1:
        print(f"not exist | {a_id}-{p_id} | {remote_path}")
    local_size = -1
    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
    print(f"before | {a_id}-{p_id} | {local_size} | {remote_size} | {local_size == remote_size}")
    if local_size == remote_size:
        print(f"skip | {a_id}-{p_id} | {local_size} | {remote_size} | {local_size == remote_size}")
        return True 

    try:    
        ftp_con.download(output_path, remote_path)
    except:
        print(f"error | {a_id}-{p_id} | {local_size} | {remote_size} | {local_size == remote_size} | {remote_path}")
        ftp_con.close()
        pass
        
    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
    if local_size != remote_size:
        remote_size = ftp_con.get_size(remote_path)
        
    ftp_con.close()
    if local_size == remote_size:
        print(f"success | {a_id}-{p_id} | {local_size} | {remote_size} | {local_size == remote_size}")
        return True
    else:
        print(f"fail | {a_id}-{p_id} | {local_size} | {remote_size} | {local_size == remote_size} | {remote_path}")
        return False
    

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
    
    for taxa in taxa_list:
        print(f"create_meta_tsv : start")
        result_dfs = Parallel(n_jobs=6)(delayed(create_meta_tsv)(taxa, p_id) for p_id in tqdm(range(800)))
        gathered_df = pd.concat(result_dfs, axis=0)
        print(f"create_meta_tsv : end")
        
        print(f"download_taxa_data : start")
        df = gathered_df[gathered_df["is_downloaded"] == False]
        dfs = np.array_split(df, n_procs*1000)
        
        t0 = time()
        for a_id, df in enumerate(dfs):
            if a_id >= 1008:
                count = 1
                t1 = time()
                while df.shape[0] != df["is_downloaded"].sum():
                    print(f"{df['is_downloaded'].sum()} | {df.shape[0]}")
                    ftp_con = FTPConnection()
                    # ftp_con.connect()
                    result = Parallel(n_jobs=6)(delayed(download_taxa_data)(ftp_con, p_id, row, a_id) for p_id, row in enumerate(tqdm(df.values)))
                    # ftp_con.close()
                    df["is_downloaded"] = result
                    sum = df["is_downloaded"].sum()
                    print(f"{count} try | {sum} | {df.shape[0]}")
                    if count == 5:
                        break
                    count += 1
                    view = df[df["is_downloaded"] == False]
                    df = view.copy()
                t2 = time()
                print(f"{t2-t1:.3f}sec | {t2-t0:.3f}sec")
            else: 
                print(f"{a_id}: skip")
        print(f"download_taxa_data : end")
            