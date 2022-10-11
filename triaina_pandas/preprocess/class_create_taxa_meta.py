'''
Created on Oct 11, 2022

@author: root
'''

import ftplib, os
import pandas as pd

class FTPConnection:
    def __init__(self, host, output_path):
        self.ftp = None
        self.host = host
        self.dh_output_path = f"{output_path}/NCBI_DH"
        self.output_path = f"{output_path}/NCBI"
        
    
    def connect(self):
        self.ftp = ftplib.FTP(self.host)
        self.ftp.login()
        
    def close(self):
        self.ftp.close()
    
    def download_assembly_summary(self, taxa):
        summary_dir = f"{self.dh_output_path}/{taxa}"
        summary_file_path = f"{summary_dir}/assembly_summary.txt"
        ftp_summary_file_path = f"genomes/genbank/{taxa}/assembly_summary.txt"
        
        # check exist summary
        print("check exist assembly_summary.txt")
        if os.path.exists(summary_file_path):
            local_summary_size = os.path.getsize(summary_file_path)
            ftp_summary_size = self.ftp.size(ftp_summary_file_path)
            # print(local_summary_size == ftp_summary_size)
            
            # compare local summary with ftp 
            if local_summary_size == ftp_summary_size:
                print("assembly_summary.txt exists already")
                return
        # check exist summary_dir
        elif not os.path.exists(summary_dir):    
            os.makedirs(summary_dir)
            
        # download assembly_summary.txt
        print("downloading assembly_summary.txt")
        with open(summary_file_path, 'wb') as fin:
            self.ftp.retrbinary(f"RETR {ftp_summary_file_path}", fin.write)
        print("download complete")
    def create_taxa_meta(self, taxa):
        summary_path = f"{self.dh_output_path}/{taxa}/assembly_summary.txt"
        df = pd.read_csv(summary_path, sep='\t', skiprows = 1, engine='python')
        df.rename(columns={"# assembly_accession": "assembly_accession"}, inplace=True)
        # print(df["assembly_accession"])
        
        # create http_path
        df["http_path"] = df["ftp_path"]
        
        # change ftp_path : https: -> ftp:
        df["ftp_path"] = df["ftp_path"].str.replace("https:", "ftp:")
        
        # create local_path
        df["local_path"] = df["ftp_path"].map(lambda ftp_path: self.set_local_path(ftp_path, taxa))
        
        # create is_download
        df["is_downloaded"] = df.apply(lambda row: self.is_downloaded(row, taxa), axis=1)
        
        list = ["assembly_accession", "taxid", " species_taxid", "organism_name", "infaspecific_name", "ftp_path", "local_path", "is_downloaded"]
        # print(df.loc[10,:])
        
        
    def set_local_path(self, ftp_path, taxa):
        file_name = ftp_path.split('/')[-1]
        
        local_path = f"{self.output_path}/{taxa}/{file_name}_genomic.fna.gz"
        
        return local_path
        
    def is_downloaded(self, row, taxa):
        local_path = row["local_path"]
        file_name = local_path.split('/')[-1]
        ftp_file_path = row["ftp_path"].split(sep='/', maxsplit=3)[-1]
        ftp_file_size = None
        try:
            ftp_file_size = self.ftp.size(f"{ftp_file_path}/{file_name}")
        except ftplib.all_errors as e:
            # print("[error]: ", e)
            # re-connect
            if str(e)[:3] == '421':
                print("connecting close")
                self.connect()
                ftp_file_size = self.ftp.size(f"{ftp_file_path}/{file_name}")
                print("re-connect")
        # check exist local file 
        if os.path.exists(local_path):
            print(f"exist {file_name}")
            local_file_size = os.path.getsize(local_path)
            if local_file_size == ftp_file_size:
                print("same size")
                return True
            else :
                print("need update")
        with open(local_path, 'wb') as fin:
            try:
                self.ftp.retrbinary(f"RETR {ftp_file_path}", fin.write)
            except ftplib.all_errors as e:
                print("[error]: ", e)
                self.connect()
                self.ftp.retrbinary(f"RETR {ftp_file_path}", fin.write)
                print("re-connect")
        
        local_file_size = os.path.getsize(local_path)
        
        if local_file_size == ftp_file_size:
            print(f"complete download: {file_name}")
            return True
        else :
            print("need download again")
            return False
            
        
        
if __name__ == '__main__':
    host = "ftp.ncbi.nlm.nih.gov"
    output_path = "/home/neuroears/data_mount/study/data"
    
    
    ftp_connection = FTPConnection(host, output_path)
    
    ftp_connection.connect()
    
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    for taxa in taxa_list:
        ftp_connection.download_assembly_summary(taxa)
        ftp_connection.create_taxa_meta(taxa)
        break
    
    ftp_connection.close()
    