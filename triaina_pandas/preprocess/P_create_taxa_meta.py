'''
Created on Oct 5, 2022

@author: root
'''

import ftplib, os
import pandas as pd

def is_downloaded(row, ftp):
    http_path = row['http_path']
    file_name = http_path.split('/')[-1]
    file_path = f"{http_path[29:]}/{file_name}_genomic.fna.gz"
    file_size = ftp.size(file_path)
    
    local_path = row["local_path"]
    if(os.path.isfile(local_path)):
        local_file_size = os.stat(local_path)
        # print(local_file_size.st_size == file_size)
        if(local_file_size.st_size == file_size):
            return True
    with open(local_path, 'wb') as fin:
        ftp.retrbinary(f'RETR {file_path}', fin.write)
    
    local_file_size = os.stat(local_path)
    return local_file_size == file_size
    
def set_local_path(ftp_path, taxa):
    default_path = f'/home/neuroears/data_mount/data/NCBI/{taxa}'
    tokens = ftp_path.split('/')
    local_path = f'{default_path}/{tokens[-1]}_genomic.fna.gz'
    return local_path

def create_taxa_meta(output_dir, ftp, taxa):
    ftp_file_path = f'genomes/genbank/{taxa}/assembly_summary.txt'
    output_file_path = f'{output_dir}/NCBI_DH/{taxa}/assembly_summary.txt'
    
    file_path = os.path.split(output_file_path)

    if not os.path.exists(file_path[0]):
        os.makedirs(file_path[0])
    # print(ftp.size(ftp_file_path))
    
    with open(output_file_path, 'wb') as fin:
        ftp.retrbinary(f'RETR {ftp_file_path}', fin.write)
        
    df = pd.read_csv(output_file_path, sep='\t', skiprows=1)
    # print(df.loc[1,'ftp_path']) # checked
    

    df['http_path'] = df['ftp_path']
    
    df['ftp_path'] = df['ftp_path'].str.replace('https:', 'ftp:')
    
    df['local_path'] = df['ftp_path'].map(lambda x : set_local_path(x, taxa))
    
    df["is_downloaded"] = df.apply(lambda row: is_downloaded(row, ftp), axis=1)
    
    df.rename(columns={"# assembly_accession": "assembly_accession"}, inplace=True)
    
    list = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "is_downloaded"]
    
    view = df[list]
    df = view.copy()
    
    print(df["is_downloaded"])
    
    tsv_path = f"{output_dir}/NCBI_DH/{taxa}/{taxa}.tsv"
    df.to_csv(tsv_path, sep='\t', index=False)

if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    output_dir = "/home/neuroears/data_mount/data"
    
    host = "ftp.ncbi.nlm.nih.gov"
    ftp = ftplib.FTP(host)
    ftp.login()
    
    for taxa in taxa_list:
        create_taxa_meta(output_dir, ftp, taxa)
        break

    ftp.close()