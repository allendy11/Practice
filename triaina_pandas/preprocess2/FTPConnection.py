'''
Created on Oct 11, 2022

@author: root
'''
import ftplib, os
import pandas as pd

class FTPConnection:
    def __init__(self, host, output_path, output_my_path):
        self.ftp = None
        self.host = host
        self.output_path = output_path # data/NCBI
        self.output_my_path = output_my_path # data/NCBI_DHDH
     
    def connect(self):  
        self.ftp = ftplib.FTP(self.host)
        self.ftp.login()
        
    def close(self):
        self.ftp.close()
        
    def download_assembly_summary(self, taxa):
        ftp_summary_path = f"genomes/genbank/{taxa}/assembly_summary.txt"
        local_summary_path = f"{self.output_my_path}/{taxa}/assembly_summary.txt"
        
        tokens = os.path.split(local_summary_path)
        
        if os.path.exists(local_summary_path):
            local_summary_size = os.path.getsize(local_summary_path)
            ftp_summary_size = self.ftp.size(ftp_summary_path)
            if local_summary_size == ftp_summary_size:
                print("Exist already: ", local_summary_path)
                return
            else:
                print("Need update: ", local_summary_path)
        else:  
            if not os.path.exists(tokens[0]):
                os.makedirs(tokens[0])
        
        with open(local_summary_path, 'wb') as fin:
            self.ftp.retrbinary(f"RETR {ftp_summary_path}", fin.write)
        
        print("Create complete: ", local_summary_path)
        
    def create_taxa_meta(self, taxa):
        local_summary_path = f"{self.output_my_path}/{taxa}/assembly_summary.txt"
        df = pd.read_csv(local_summary_path, sep="\t", skiprows=1)
        df.rename(columns = {"# assembly_accession": "assembly_accession"}, inplace=True)
        # print(df.columns)
        
        df["http_path"] = df["ftp_path"]
        
        df["ftp_path"] = df["ftp_path"].str.replace("https:", "ftp:")
        # print(df["ftp_path"])
        
        df["local_path"] = df["ftp_path"].map(lambda ftp_path: self.set_local_path(ftp_path, taxa))
        # print(df["local_path"])
        
        df["is_downloaded"] = df.apply(lambda row: self.is_downloaded(row, taxa), axis=1)
        list = ["assembly_accession", " taxid", "species_taxid", "organism_name", "infraspecific_name", "ftp_path", "local_path", "is_downloaded"]
        view = df[list]
        df = view.copy()
        
        return df
    
    def set_local_path(self, ftp_path, taxa):
        file_name = os.path.split(ftp_path)[-1]
        local_path = f"{self.output_path}/{taxa}/{file_name}_genomic.fna.gz"
        return local_path
        
    def is_downloaded(self, row, taxa):   
        local_path = row["local_path"]
        file_name = os.path.split(local_path)[-1]
        ftp_file_path = f"{row['ftp_path'].split(sep='/', maxsplit=3)[-1]}/{file_name}"
        
        try:
            ftp_file_size = self.ftp.size(ftp_file_path)
        except ftplib.all_errors as e:
            print(f"Error {str(e)[:3]} closed connection: re-connecting...")
            self.connect()
            ftp_file_size = self.ftp.size(ftp_file_path)
                
        if os.path.exists(local_path):
            local_file_size = os.path.getsize(local_path)
            if local_file_size == ftp_file_size:
                print("No need update: ", file_name)
                return True
         
        with open(local_path, 'wb') as fin:
            try:
                self.ftp.retrbinary(f"RETR {ftp_file_path}", fin.write)
            except ftplib.all_errors as e:
                print(f"Error {str(e)[:3]} closed connection: re-connecting...")
                self.connect()
                self.ftp.retrbinary(f"RETR {ftp_file_path}", fin.write)       
                     
        local_file_size = os.path.getsize(local_path)
        if local_file_size == ftp_file_size:
            print("Download complete: ", file_name)
            return True
        else:
            print("Need download, try again: ", file_name)
            return False
            
        
        
        
        
        
        
        
            
        