'''
Created on 20 Oct 2022

@author: root
'''

import os
import pandas as pd
from preprocess.FTPConnection import FTPConnection
from pickle import NONE


def set_local_path(ftp_path, taxa):
    local_dir = f"/Volumes/study/data/NCBI/{taxa}"
    file_name = os.path.basename(ftp_path)
    local_path = f"{local_dir}/{file_name}_genomic.fna.gz"
    return local_path


def modify_summary(output_path, taxa):
    df = pd.read_csv(output_path, sep='\t', skiprows=1, low_memory=False)
    df.rename(
        columns={"# assembly_accession": "assembly_accession"}, inplace=True)
    df = df[df["ftp_path"] != "na"].copy()
    df["http_path"] = df["ftp_path"]
    df["ftp_path"] = df["ftp_path"].str.replace("http", "ftp")
    df["local_path"] = df["ftp_path"].map(lambda x: set_local_path(x, taxa))
    return df


def download_summary(output_path, taxa, is_purge=False):
    if os.path.exists(output_path) and not is_purge:
        print("download_summary : skip process")
        df = modify_summary(output_path, taxa)
        return df
    else:
        print("download_summary")

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()

    remote_path = f"/genomes/genbank/{taxa}/assembly_summary.txt"
    ftp_con.download(output_path, remote_path)
    print("downloaded")
    ftp_con.close()

    df = modify_summary(output_path, taxa)
    return df


def get_size(ftp, row, df_len, taxa, p_id):
    output_path = row["local_path"]
    file_name = os.path.basename(output_path)

    local_size = -1
    remote_size = -1

    if not os.path.exists(output_path):
        row["is_downloaded"] = False
    else:
        local_size = os.path.getsize(output_path)
        row["local_size"] = local_size

    remote_dir = (row["ftp_path"].split(sep='/', maxsplit=3))[-1]
    remote_path = f"{remote_dir}/{file_name}"

    try:
        remote_size = ftp.get_size(remote_path)
    except:
        print(f"Error[get_size] : {taxa}_{p_id}_{row.name} : {file_name}")
        remote_size = -1
    # if 0 == row.name % 100:
    print(f"[get_size]\t[{(row.name/df_len)*100:.1f}%]\t[{taxa}_{p_id}]\t[{row.name}/{df_len}]\t[{local_size == remote_size} {local_size}/{remote_size}]\t[{file_name}]")

    row["remote_path"] = remote_path
    row["remote_size"] = remote_size

    if -1 == remote_size or -1 == local_size:
        row["is_downloaded"] = False
    row["is_downloaded"] = (remote_size == local_size)

    return row


def get_remote_size(output_path, df, taxa, p_id=None, is_purge=False):
    # if 42 > p_id:
    #     return pd.DataFrame()
    df_len = len(df)
    print(f"core_{p_id}, total: {df_len}")

    tsv_path = f"{output_path}.{p_id}"
    if os.path.exists(tsv_path) and not is_purge:
        df = pd.read_csv(tsv_path, sep='\t')
        return df

    df.reset_index(inplace=True)
    tsv_tmp_path = f"{tsv_path}.tmp"
    df.to_csv(tsv_tmp_path, sep='\t', index=False)

    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()
    # df = df.iloc[::-1]
    df = df.apply(lambda row: get_size(
        ftp_con, row, len(df), taxa, p_id), axis=1)

    ftp_con.close()

    lst = ["assembly_accession", "taxid", "species_taxid", "organism_name", "infraspecific_name",
           "ftp_path", "local_path", "remote_path", "local_size", "remote_size", "is_downloaded"]
    view = df[lst]
    df = view.copy()
    df.to_csv(tsv_path, sep='\t', index=False)
    return df


def is_downloaded(ftp, row, taxa, df_len, p_id):
    remote_path = row["remote_path"]
    output_path = row["local_path"]
    remote_size = row["remote_size"]
    file_name = os.path.basename(output_path)

    if remote_size == -1:
        return row

    try:
        ftp.download(output_path, remote_path, remote_size)
    except:
        print(f"Error[is_download]: {taxa}_{p_id} {row.name} ${file_name}")

    local_size = os.path.getsize(output_path)
    print(f"[is_downloaded]\t[{(row.name/df_len)*100:.1f}%]\t[{taxa}_{p_id}]\t[{row.name}/{df_len}]\t[{local_size == remote_size} {local_size}/{remote_size}]\t[{file_name}]")
    row["is_downloaded"] = True
    return row


def get_remote_data(df, taxa, p_id=None, is_purge=False):
    # tsv_path = f"{output_path}.{p_id}"
    # if os.path.exists(tsv_path) and not is_purge:
    #     print("download_taxa : skip process")
    #     return df
    df.reset_index(inplace=True)

    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()

    df = df.apply(lambda row: is_downloaded(
        ftp_con, row, taxa, len(df), p_id), axis=1)

    ftp_con.close()

    return df


if __name__ == '__main__':
    pass
    # is_purge = False
    # taxa = "archaea"
    # summary_output_path = f"/home/neuroears/data_mount/study/data/NCBI_DH/{taxa}/assembly_summary.txt"
    # taxa_output_dir = f"/home/neuroears/data_mount/study/data/NCBI/{taxa}"
    #
    # df = download_summary(summary_output_path, taxa, is_purge)
    #
    # df = get_remote_size(summary_output_path, df, p_id=None, is_purge=is_purge)
