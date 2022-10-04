'''
Created on Sep 29, 2022

@author: neuroears
'''

import ftplib, os
import pandas as pd
import timeit

def save_to_pickle(df, output_dir, taxa):
    output_pkl_path = f'{output_dir}/{taxa}.pkl'
    return df.to_pickle(output_pkl_path, index=False, sep='\t')
   
def save_to_tsv(df, output_dir, taxa):
    output_tsv_path = f'{output_dir}/{taxa}.tsv'
    return df.to_csv(output_tsv_path, index=False, sep='\t')

def get_local_path(ftp_path, taxa):
    default_path = f"/home/neuroears/data_mount/data/NCBI/{taxa}/"
    # file_name = "_genomic.fna.gz"
    tokens = ftp_path.split('/')
    local_path = default_path + tokens[-1]
    return local_path  

def get_http_path(ftp_path, taxa):
    default_path = f"/home/neuroears/data_mount/data/NCBI/{taxa}/"
    file_name = "_genomic.fna.gz"
    tokens = ftp_path.split('/')
    http_path = default_path + tokens[-1] + file_name
    return http_path  

def create_taxa_meta(output_dir, ftp, taxa):
    output_file_path = f'{output_dir}/assembly_summary.txt'
# 1-1. Download assembly_summary.txt for each taxa using ftplib
    # input_file_path = f'genomes/genbank/{taxa}/assembly_summary.txt'
    # ftp = ftplib.FTP(host)
    # ftp.login()
    # with open(output_file_path, 'wb') as fin:
    #     ftp.retrbinary(f'RETR {input_file_path}', fin.write)
    # ftp.close()
    
# 1-2. Check a ftp_path value using internet browser by typing it
# 1-3. Confirm the final ftp_path to those ending with _genomic.fna.gz
    df = pd.read_csv(output_file_path, sep='\t', skiprows=1)
    df.rename(columns = {"# assembly_accession": "assembly_accession"}, inplace=True)
    df['ftp_path'] = df["ftp_path"].map(lambda x: x+"_genomic.fna.gz")
   

    
# 1-4. df["http_path"] = df["ftp_path"]
    df["http_path"] = df["ftp_path"]
# 1-5. Change the ftp_path column (https: to ftp:)
    df["ftp_path"] = df["ftp_path"].str.replace("https:", "ftp:")

# 1-6. Create a local_path column from the ftp_path column
    df["local_path"] = df["ftp_path"].map(lambda x: get_local_path(x, taxa))    
    # print(df.loc[4,"local_path"].split('/'))

# 1-7. Save pandas df to .tsv
# 1-8. Save pandas df to pickle
# 1-9. Compare the performance 1-7, 1-8 using timeit
    df["is_downloaded"] = False
    list = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "is_downloaded"]
    view = df[list]
    df = view.copy()
    
    def save_to_pickle():
        output_pkl_path = f'{output_dir}/{taxa}.pkl'
        return df.to_pickle(output_pkl_path, index=False, sep='\t')
    
    def save_to_tsv():
        output_tsv_path = f'{output_dir}/{taxa}.tsv'
        return df.to_csv(output_tsv_path, index=False, sep='\t')
    
    time_tsv = timeit.timeit('save_to_tsv()', 'from __main__ import save_to_tsv, df, output_dir, taxa', number=1)
    # time_pickle = timeit.timeit(stmt=save_to_pickle(), number=1)
    print("tsv: ",time_tsv)
    # print("pkl: ", time_pickle)
    

    # stmt="pass", setup="pass", timer=default_timer, repeat=default_repeat, number=default_number, globals=None
    
    # def test():
    #     return "-".join(str(n) for n in range(100))
    #
    # t1 = timeit.timeit(stmt=test(), number=10000)
    # print(t1)
    
    
if __name__ == '__main__':
    host = 'ftp.ncbi.nlm.nih.gov'
    
    output_dir = f'/home/neuroears/data/NCBI_DH'
    # output_dir = f'/home/neuroears/data_mount/data/NCBI_DH/assembly_summary.txt' 
    input_file_path = f'genomes/genbank/archaea/assembly_summary.txt'
    
    # taxa_list = ["archaea", "viral", "protozoa", "fungi", "bacteria"]
    #
    # ftp = ftplib.FTP(host)
    #
    # for taxa in taxa_list:
    #     create_taxa_meta(output_dir, ftp, taxa)
    #     break;
    
    ftp = ftplib.FTP(host)
    output_file_path = f'{output_dir}/assembly_summary.txt'
    ftp.login()
    with open(output_file_path, 'wb') as fin:
        ftp.retrbinary(f'RETR {input_file_path}', fin.write)
    
    
    df = pd.read_csv(output_file_path, sep='\t', skiprows=1)
    # print(df.head(1))
    df.rename(columns = {"# assembly_accession": "assembly_accession"}, inplace=True)
    # df["ftp_path"] = df["ftp_path"].map(lambda x: x+"_genomic.fna.gz")
    # print(df.loc[4,"ftp_path"].split('/')[-1])
    df["http_path"] = df["ftp_path"]
    df["ftp_path"] = df["ftp_path"].str.replace("https:" , "ftp:")
    # print(df["ftp_path"])
    
    def get_local_path(ftp_path):
        default_path = "/home/neuroears/data_mount/data/NCBI/archaea/"
        tokens = ftp_path.split('/')
        local_path = default_path + tokens[-1]
        # print(local_path)
        return local_path
    df["local_path"] = df["ftp_path"].map(lambda x: get_local_path(x))
    
    # print(df["local_path"])
    def is_downloaded(row, ftp):
        path = row["http_path"][29:]
        # print(path)
        # list = ftp.nlst(path)
        # print(list)
        size = ftp.size(f'{path}_genomic.fna.gz')
        
        # pwd = ftp.pwd()
        # list = ftp.nlst('genomes/all/GCA')
        # print(list)
        
        # s = row["http_path"][29:]
        # print(s)
        # size = ftp.size(s)
        # print(size)

        # tokens = row["http_path"].split('/')
        # print(tokens[-1])
        # size = ftp.size(tokens[-1])
        # print(size)
        
        
    df["is_downloaded"] = df.apply(lambda row: is_downloaded(row, ftp), axis=1)
    
    
    # list = ["assembly_acession", "taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "is_downloaded"]
    # view = df[list]
    # df = view.copy()
    #
    # output_tsv_path = f'{output_dir}/arhaea.tsv'
    # df.to_csv(output_tsv_path, index=False, sep='\t')
    #
    # output_pkl_path = f'{output_dir}/arhaea.pkl'
    # df.to_pickle(output_pkl_path)
    
    ftp.close()
    
    
    
    