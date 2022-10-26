'''
Created on Oct 24, 2022

@author: root
'''

import pandas as pd
import os
from preprocess.FTPConnection import FTPConnection
from unittest.mock import inplace

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
    print("create_taxa_meta: start")
    if os.path.exists(output_path) and not is_purge:
        print("skip download summary")
        df = modify_taxa_meta(output_path, taxa)
        print("create_taxa_meta: end")
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
    print("create_taxa_meta: end")

    return df


def get_remote_size(row, ftp_con, df_len, taxa, p_id):
    output_path = row["local_path"]
    file_name = os.path.basename(output_path)
    ftp_path = row["ftp_path"]
    remote_dir = (ftp_path.split(sep='/', maxsplit = 3))[-1]
    remote_path = f"{remote_dir}/{file_name}"
    row["remote_path"] = remote_path
    
    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
    else:
        local_size = -1
    
    try:
        remote_size = ftp_con.get_size(remote_path)
    except:
        print(f"Err : {taxa}-{p_id} {remote_path}")
        remote_size = -1
        
    print(f"[get_remote_size] {(row.name/df_len)*100:.1f}% | {taxa}-{p_id} | {row.name}/{df_len} | {local_size}/{remote_size} | {remote_path}")
    
    row["remote_size"] = remote_size
    
    if local_size == -1 | remote_size == -1:
        row["is_downloaded"] = False
    else:
        if remote_size == local_size:
            row["is_downloaded"] = True
        else:
            row["is_downlaoded"] = False
    return row
    
    


def set_remote_size(output_path, df, taxa, p_id, is_purge):
    # if p_id > 400:
    #     print(f"skip: {p_id}")
    #     return pd.DataFrame()
    #

    df_len = len(df)
    print(f"[set_remote_size] {taxa}-{p_id}-{df_len}")
    tsv_path = f"{output_path}.{p_id}"
    if os.path.exists(tsv_path) and not is_purge:
        print(f"[set_remote_size] {taxa}-{p_id}-{df_len} | skip")
        df = pd.read_csv(tsv_path, sep='\t')
        return df
    print(f"[set_remote_size] {taxa}-{p_id}-{df_len}")
    # df.reset_index(inplace=True)
    
    tsv_tmp_path = f"{tsv_path}.tmp"
    df.to_csv(tsv_tmp_path, sep='\t', index=False)
    
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()
    
    df = df.apply(lambda row : get_remote_size(row, ftp_con, df_len, taxa, p_id), axis=1)
    
    ftp_con.close()
    
    lst = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "remote_path", "remote_size", "is_downloaded"]
    view = df[lst]
    df = view.copy()
    df.to_csv(tsv_path, sep='\t', index=False)
    return df


def is_downloaded(row, ftp_con, df_len, taxa, p_id):
    remote_path = row["remote_path"]
    output_path = row["local_path"]
    local_size = os.path.getsize(output_path)
    remote_size = row["remote_size"]
    
    if local_size == remote_size:
        print("Downloaded already")
        return row
    
    if remote_size == -1:
        print("Not found remote file")
        return row
    
    try:
        ftp_con.download(output_path, remote_path, remote_size)
    except:
        print(f"Err : {taxa}-{p_id} {remote_path}")
        return row
    
    local_size = os.path.getsize(output_path)
    print(f"[get_remote_size] {(row.name/df_len)*100:.1f}% | {taxa}-{p_id} | {row.name}/{df_len} | {local_size}/{remote_size} | {remote_path}")

    row["is_downloaded"] = True
    
    return row

def download_taxa_data(df, taxa, p_id, is_purge):
    df_len = len(df)
    df.reset_index(inplace=True)
    
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()
    
    df = df.apply(lambda row : is_downloaded(row, ftp_con, df_len, taxa, p_id), axis=1)
    
    ftp_con.close()

    return df
    
if __name__ == '__main__':
    pass
    # taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    # for taxa in taxa_list:
    #     df = create_taxa_meta(taxa)
    #
    #
    #     df_ = df[~df["is_downloaded"]]
    #
    #     download_taxa_data(df_)
    #
    #     print(f"{t4-t1:.3f} sec")