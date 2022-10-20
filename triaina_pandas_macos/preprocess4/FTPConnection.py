'''
Created on 19 Oct 2022

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
            err_code = str(e)[:3]
            print("ERROR : ", err_code, remote_path, end=" ")
            if (err_code == "421"):
                print("Connection closed. Re-connect...")
                self.connect()
                size = self.ftp.size(remote_path)
            elif (err_code == "550"):
                print("Not found file")
                size = -1
            else:
                print(str(e), "Re-connect...")
                self.connect()
                size = self.ftp_size(remote_path)
        return size

    # put remote_size 10.19 10:11am
    def download(self, output_path, remote_path, remote_size=-1):
        local_size = None
        if -1 == remote_size:
            remote_size = self.get_size(remote_path)
        if os.path.exists(output_path):
            local_size = os.path.getsize(output_path)
            if remote_size == local_size:
                return
        if remote_size == -1:
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
