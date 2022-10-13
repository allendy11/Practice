'''
Created on Oct 12, 2022

@author: root
'''

import os
import pandas as pd
from preprocess.FTPConnection import FTPConnection

def create_pkl(df, taxa):
    output_path = f"/home/allen/data_mount/study/data/NCBI_DH/{taxa}.pkl"
    df.to_pkl(output_path)
    
def create_tsv(df, taxa):
    output_path = f"/home/allen/data_mount/study/data/NCBI_DH/{taxa}.tsv"
    df.to_csv(output_path, sep='\t', index=False)
    
def is_downloaded(row, ftp_con):
    output_path = row["local_path"]
    file_name = os.path.basename(output_path)
    remote_dir = row["ftp_path"].split(sep='/', maxsplit=3)
    remote_path = f"{remote_dir[-1]}/{file_name}"
    
    # check exist output_path
    if os.path.exists(output_path):
        # compare size
        output_size = os.path.getsize(output_path)
        remote_size = ftp_con.get_size(remote_path)
        if output_size == remote_size:
            print("pass")
            return True
    
    ftp_con.download(output_path, remote_path)
    print("downloaded: ", file_name)
    return True
    
def set_local_path(ftp_path, taxa):
    output_dir = f"/home/allen/data_mount/study/data/NCBI/{taxa}"
    
    # create output_dir 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_name = os.path.basename(ftp_path)
    local_path = f"{output_dir}/{file_name}_genomic.fna.gz"
    return local_path


def download_taxa_data(df, id=None):
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    df["is_downloaded"] = df.apply(lambda row: is_downloaded(row, ftp_con), axis=1)
    ftp_con.close()
    
    list = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "is_downloaded"]
    
    return df[list]
    
def modify_taxa_meta(df, taxa):
    df["http_path"] = df["ftp_path"]
    df["ftp_path"] = df["ftp_path"].str.replace("https:", "ftp:")
    df["local_path"] = df["ftp_path"].map(lambda x: set_local_path(x, taxa))
    return df
    
def create_taxa_meta(taxa):
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    
    remote_path = f"genomes/genbank/{taxa}/assembly_summary.txt"
    output_path = f"/home/allen/data_mount/study/data/NCBI_DH/{taxa}/assembly_summary.txt"
    
    # check exist output_path
    if not os.path.exists(output_path):
        # check exist output_dir
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        ftp_con.download(output_path, remote_path)   
    else:  
        # compare size
        local_size = os.path.getsize(output_path)
        remote_size = ftp_con.get_size(remote_path)
        if not local_size == remote_size:
            ftp_con.download(output_path, remote_path)
            
    ftp_con.close()
    
    df = pd.read_csv(output_path, sep="\t", skiprows=1)
    df.rename(columns={"# assembly_accession": "assembly_accession"}, inplace=True)
    return df

if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    
    
    for taxa in taxa_list:
        df = create_taxa_meta(taxa)
        df = modify_taxa_meta(df, taxa)
        df = download_taxa_data(df)
        create_tsv(df)
        break
