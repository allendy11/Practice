'''
Created on 14 Oct 2022

@author: allen
'''

import ftplib


class FTPConnection:

    def __init__(self):
        self.ftp = None

    def set_host(self, host):
        self.host = host

    def connect(self):
        self.ftp = ftplib.FTP(self.host)
        self.login()
        print("[connection success]")

    def login(self):
        self.ftp.login()

    def close(self):
        self.ftp.close()
        print("[connection closed]")

    def get_size(self, remote_path):
        size = None
        try:
            size = self.ftp.size(remote_path)
        except ftplib.all_errors as e:
            print(e, "re-connect...")
            self.connect()
            size = self.ftp.size(remote_path)
        return size

    def download(self, output_path, remote_path):
        with open(output_path, 'wb') as fin:
            try:
                self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
            except ftplib.all_errors as e:
                print(e, "re-connect...")
                self.connect()
                self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
