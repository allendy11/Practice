'''
Created on 18 Oct 2022

@author: root
'''

import ftplib
import os


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
        local_size = None
        if os.path.exists(output_path):
            local_size = os.path.getsize(output_path)
        remote_size = self.get_size(remote_path)
        if remote_size == local_size:
            return

        while True:
            with open(output_path, 'wb') as fin:
                try:
                    self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
                except ftplib.all_errors as e:
                    print(e, "re-connect...")
                    self.connect()
                    self.ftp.retrbinary(f"RETR {remote_path}", fin.write)
            local_size = os.path.getsize(output_path)
            if remote_size == local_size:
                break
            print(f"remote_size : {remote_size}, local_size: {local_size}")
