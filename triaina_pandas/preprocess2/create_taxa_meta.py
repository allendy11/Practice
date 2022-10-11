'''
Created on Oct 11, 2022

@author: root
'''
import pandas as pd
from preprocess2.FTPConnection import FTPConnection

def create_taxa_meta(taxa):
    host = "ftp.ncbi.nlm.nih.gov"
    output_path = "/home/allen/data_mount/study/data/NCBI"
    output_my_path = "/home/allen/data_mount/study/data/NCBI_DHDH"
    ftp_connection = FTPConnection(host, output_path, output_my_path)
    ftp_connection.connect()
    ftp_connection.download_assembly_summary(taxa)
    
    df = ftp_connection.create_taxa_meta(taxa)
    
    ftp_connection.close()
    
    tsv_path = f"{output_my_path}/{taxa}.tsv"
    df.to_csv(tsv_path, sep='\t', index=False)
    
    
if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    for taxa in taxa_list:
        create_taxa_meta(taxa)
        break