'''
Created on Nov 7, 2022

@author: root
'''

import ftplib

class FTPConnection(object):
    def __init__(self):
        self.ftp = None
    
    def set_host(self, host):
        self.host = host
    
    def connect(self):
        self.ftp = ftplib.FTP("ftp.ncbi.nlm.nih.gov")
        self.login()
    
    def login(self):
        self.ftp.login()
    
    def close(self):
        self.ftp.close()
        
    def get_size(self, path):
        size = -1
        try:
            size = self.ftp.size(path)
        except ftplib.all_errors as e:
            err_code = str(e)[:3]
            if err_code == "421":
                self.connect()
                size = self.ftp.size(path)
            else:
                print(e)
                pass
        return size
    
    def download(self, output_path, remote_path):
        with open(output_path, 'wb') as fin:
            try:
                self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
            except ftplib.all_errors as e:
                print(e)
                self.ftp.retrbinary(f"RETR {remote_path}", fin.write)