'''
Created on Nov 1, 2022

@author: root
'''

import ftplib, os, time

class FTPConnection(object):
    def __init__(self):
        self.ftp = None
    
    def set_host(self, host):
        self.host = host
    
    def connect(self):
        print("[FTP connecting...]")
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
                # print("[Error 421]: ", e,  "re-connecting...")
                self.connect()
                size = size = self.ftp.size(remote_path)
            elif err_code == "550":
                # print("[Error 550]: ", e)
                size = -1
            else:
                # print("[Err unknown]: ", e)
                size = -1
        return size
    
    def download(self, output_path, remote_path, local_size, remote_size):
        count = 1
        
        while True:
            with open(output_path, 'wb') as fin:
                try:
                    self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
                except ftplib.all_errors as e:
                    err_code = str(e)[:3]
                    if err_code == "421":
                        # print(f"reconnecting...")
                        time.sleep(5)
                        self.connect()
                        self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
                    elif err_code == "550":
                        # print(f"Not found remote_file: {remote_path}")
                        return {'result': False, 'error': e}
                    else:
                        # print(f"Unknown Error: {e}")
                        return {'result': False, 'error': e}
            local_size = os.path.getsize(output_path)
            if local_size == remote_size:
                break
            if count == 10:
                break
            count += 1
        return {'result': True, 'error': None}
