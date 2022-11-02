'''
Created on Nov 1, 2022

@author: root
'''

import os
import pandas as pd
from preprocess.FTPConnection import FTPConnection
from random import random
from time import time, sleep

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


def create_taxa_meta(output_path, taxa, is_purge):
    print(f"[create_assembly_summay] : start")
    
    if os.path.exists(output_path) and not is_purge:
        print(f"[create_assembly_summay] : skip download")
        df = modify_taxa_meta(output_path, taxa)
        print(f"[create_assembly_summay] : end")
        return df

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()
    
    remote_path = f"genomes/genbank/{taxa}/assembly_summary.txt"
    ftp_con.download(output_path, remote_path)
    ftp_con.close()
    
    df = modify_taxa_meta(output_path, taxa)
    print(f"[create_assembly_summay] : end")
    
    return df


def get_remote_size(row, ftp_con, df_len, taxa, id):   
    output_path = row["local_path"]
    file_name = os.path.basename(output_path)
    ftp_path = row["ftp_path"]
    remote_dir = (ftp_path.split(sep='/', maxsplit = 3))[-1]
    remote_path = f"{remote_dir}/{file_name}"

    row["remote_path"] = remote_path
    
    local_size = -1
    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
    
    remote_size = -1
    try:
        remote_size = ftp_con.get_size(remote_path)
        print(f"[get_remote_size] SUCCESS : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | remote_size: {remote_size}")
    except:
        print(f"[get_remote_size] FAIL : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | remote_size: {remote_size}")
        
    row["remote_size"] = remote_size
    
    row["is_downloaded"] = False;
    if local_size != -1 | remote_size != -1:
        if local_size == remote_size:
            row["is_downloaded"] = True
    
    return row


def create_meta_tsv(output_path, df, taxa, id, is_purge):
    df_len = len(df)
    
    tsv_path = f"{output_path}.{id}"
    if os.path.exists(tsv_path) and not is_purge:
        print(f"[create_meta_tsv] SKIP : Core_{id}")
        df = pd.read_csv(tsv_path, sep='\t')
        return df
    df.reset_index(inplace=True)
    
    # tsv_tmp_path = f"{tsv_path}.tmp"
    # if not os.path.exists(tsv_tmp_path):
    #     df.to_csv(tsv_tmp_path, sep='\t', index=False)
    
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()
    
    df = df.apply(lambda row : get_remote_size(row, ftp_con, df_len, taxa, id), axis=1)
    
    ftp_con.close()
    
    lst = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "remote_path", "remote_size", "is_downloaded"]
    view = df[lst]
    df = view.copy()
    df.to_csv(tsv_path, sep='\t', index=False)
    
    return df


def is_downloaded(row, ftp_con, df_len, taxa, id):
    remote_path = row["remote_path"]
    output_path = row["local_path"]
    file_name = os.path.basename(output_path)
    
    local_size = -1
    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
    remote_size = row["remote_size"]
    
    if remote_size == -1:
        print(f"[is_downloaded] FAIL : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | local_size: {local_size} | remove_size: {remote_size} | error: Not found file on remote_path")
        return row;
    if local_size == remote_size:
        print(f"[is_downloaded] SKIP : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | local_size: {local_size} | remove_size: {remote_size}")
        row["is_downloaded"] = True
        return row
    
    result_data = {}
    try:
        result_data = ftp_con.download(output_path, remote_path, local_size, remote_size)       
    except:
        print(f"[is_downloaded] ERROR : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | local_size: {local_size} | remove_size: {remote_size}")            
    
    local_size = -1
    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
    
    if result_data['result']:
        print(f"[is_downloaded] SUCCESS : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | local_size: {local_size} | remove_size: {remote_size}")            
    else:
        print(f"[is_downloaded] FAIL : Core_{id} | {row.name}/{df_len} | {(row.name/df_len)*100:.1f}% | local_size: {local_size} | remove_size: {remote_size} | error: {result_data['error']}")
    
    n = round(random(),3) * 5
    sleep(n) 
    
    
    
    return row
    
        


def download_taxa_data(df, taxa, id, is_purge):
    df_len = len(df)
    df.reset_index(inplace=True)
    
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()

    df = df.apply(lambda row : is_downloaded(row, ftp_con, df_len, taxa, id), axis=1)
    
    ftp_con.close()

    return df

if __name__ == '__main__':
    pass




