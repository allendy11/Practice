'''
Created on Oct 24, 2022

@author: root
'''

import ftplib, os

class FTPConnection(object):
    def __init__(self):
        self.ftp = None
    
    def set_host(self, host):
        self.host = host
    
    def connect(self):
        self.ftp = ftplib.FTP(self.host)
        self.login()
        print("[FTP connected]")
    
    def login(self):
        self.ftp.login()
    
    def close(self):
        self.ftp.close()
        
    def get_size(self, remote_path):
        size = None
        try:
            size = self.ftp.size(remote_path)
        except ftplib.all_errors as e:
            err_code = str(e)[:3]
            if err_code == "421":
                print("[Err 421]: ", e,  "re-connecting...")
                self.connect()
                size = size = self.ftp.size(remote_path)
            elif err_code == "550":
                print("[Err 550]: ", e)
                size = -1
            else:
                print("[Err unknown]: ", e)
                size = -1
        return size
    
    def download(self, output_path, remote_path, remote_size=None):
        if remote_size == None:
            remote_size = self.get_size(remote_path)
        count = 0
        while True:
            with open(output_path, 'wb') as fin:
                try:
                    self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
                except ftplib.all_errors as e:
                    err_code = str(e)[:3]
                    if err_code == "421":
                        print("[Err 421]: ", e, "re-connecting...")
                        self.connect()
                        self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
                    elif err_code == "550":
                        print("[Err 550]: ", e)
                    else:
                        print("[Err unknown]: ", e)
            local_size = os.path.getsize(output_path)
            if local_size == remote_size:
                break
            if count == 10:
                break
            count +=1
        print(f"[local_size] : {local_size}, [remote_size]: {remote_size}")
                
                