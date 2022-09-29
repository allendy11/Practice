'''
Created on Sep 28, 2022

@author: neuroears
'''

import pandas as pd
import os.path

def get_local_path(ftp_path):
    default_path = "/home/neuroears/data_mount/data/NCBI/archaea/"
    file_name = "_genomic.fna.gz"
    tokens = ftp_path.split('/')
    local_path = default_path + tokens[-1] + file_name
    return local_path  

def is_downloaded(local_path):
    downloaded = os.path.exists(local_path)
    return downloaded

def check_download_states(taxa):
    input_path = f"/home/neuroears/data_mount/data/NCBI/{taxa}/assembly_summary.txt"
    df = pd.read_csv(input_path, sep='\t', skiprows=1)
    df.rename(columns = {"# assembly_accession": "assembly_accession"}, inplace=True)
    list = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path"]
    view = df[list]
    # print(view.head(1))
    df = view.copy()
    df["local_path"] = df["ftp_path"].map(lambda x: get_local_path(x))
    df["is_downloaded"] = df["local_path"].map(lambda x : is_downloaded(x))
    print(df.head(1))
    
if __name__ == '__main__':
    taxa_list = ["archaea", "viral", "protozoa", "fungi", "bacteria"]
    for taxa in taxa_list:
        check_download_states(taxa)