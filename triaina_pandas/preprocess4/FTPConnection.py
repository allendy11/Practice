'''
Created on Oct 12, 2022

@author: root
'''

import ftplib

class FTPConnection(object):

    def __init__(self):
        self.ftp = None
    
    def connect(self):
        self.ftp = ftplib.FTP(host=self.host)
        self.ftp.login()
        
    def set_host(self, host): 
        self.host = host  
        self.connect()
        
    def close(self):
        self.ftp.close()
    
    def download(self, output_path, remote_path):
        with open(output_path, 'wb') as fin:
            try:
                self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
            except ftplib.all_errors as e:
                print(str(e), "re-connect...")
                self.connect()
                self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
    
    def get_size(self, path):
        try:
            size = self.ftp.size(path)
        except ftplib.all_errors as e:
            print(str(e), "re-connect...")
            self.connect()
            size = self.ftp.size(path)
        return size