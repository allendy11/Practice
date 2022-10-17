'''
Created on 14 Oct 2022

@author: allen
'''

import os
import pandas as pd
from preprocess.FTPConnection import FTPConnection


def download_summary(taxa):
    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()

    output_path = f"/Volumes/study/data/NCBI_DH/{taxa}/assembly_summary.txt"
    remote_path = f"genomes/genbank/{taxa}/assembly_summary.txt"

    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
        remote_size = ftp_con.get_size(remote_path)
        if local_size == remote_size:
            print("exsit metadata")

        else:
            print("update metadata...")
            ftp_con.download(output_path, remote_path)
            print("downloaded")
    else:
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        ftp_con.download(output_path, remote_path)
        print("downloaded")
    ftp_con.close()

    df = pd.read_csv(output_path, sep='\t', skiprows=1)
    df.rename(
        columns={"# assembly_accession": "assembly_accession"}, inplace=True)
    return df


def set_local_path(ftp_path, taxa):
    local_dir = f"/Volumes/study/data/NCBI/{taxa}"

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    file_name = os.path.basename(ftp_path)
    local_path = f"{local_dir}/{file_name}_genomic.fna.gz"
    return local_path


def modify_taxa_meta(df, taxa):
    df["http_path"] = df["ftp_path"]
    df["ftp_path"] = df["ftp_path"].str.replace("https", "ftp")
    df["local_path"] = df["ftp_path"].map(lambda x: set_local_path(x, taxa))
    print("modified metadata")
    return df


def is_downloaded(row, ftp_con, taxa, p_id):
    if p_id != None:
        print(f"{taxa}_{p_id} {row.name}", end='')
    else:
        print(f"{taxa} {row.name}", end='')

    output_path = row["local_path"]
    file_name = os.path.basename(output_path)
    remote_dir = (row["ftp_path"].split(sep='/', maxsplit=3))[-1]
    remote_path = f"{remote_dir}/{file_name}"
    remote_size = ftp_con.get_size(remote_path)

    if os.path.exists(output_path):
        local_size = os.path.getsize(output_path)
        if remote_size == local_size:
            print("TRUE")
            return True
    print("FALSE")
    return False


def check_is_downloaded(df, taxa, p_id=None):
    df_len = len(df)
    if p_id == None:
        print(f"{taxa} total: {df_len}")
    else:
        print(f"{taxa}_{p_id} total: {df_len}")

    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()

    df["is_downloaded"] = df.apply(
        lambda row: is_downloaded(row, ftp_con, taxa, p_id), axis=1)
    ftp_con.close()

    list = ["assembly_accession", "taxid", "species_taxid", "organism_name",
            "infraspecific_name", "ftp_path", "local_path", "is_downloaded"]
    view = df[list]
    df = view.copy()
    return df[df["is_downloaded"] == False]


def data_download(row, ftp_con, taxa, p_id, df_len):

    output_path = row["local_path"]
    file_name = os.path.basename(output_path)
    remote_dir = row["ftp_path"].split(sep='/', maxsplit=3)
    remote_path = f"{remote_dir[-1]}/{file_name}"

    if p_id != None:
        print(f"{taxa}_{p_id} {row.name} : {file_name}")
    else:
        print(f"{taxa} {row.name} : {file_name}")
    ftp_con.download(output_path, remote_path)

    print("downloaded")

    return True


def create_data_file(file_type, df, taxa, p_id):
    file_name = f"{taxa}"
    output_dir = f"/Volumes/study/data/NCBI_DH/{taxa}"
    if not p_id == None:
        file_name = f"{file_name}-{p_id}"
    if file_type == "tsv":
        output_path = f"{output_dir}/{file_name}.tsv"
        df.to_csv(output_path, sep='\t', index=False)
    elif file_type == "pkl":
        output_path = f"{output_dir}/{file_name}.pkl"
        df.to_pkl(output_path)


def download_taxa_data(df, taxa, p_id=None):
    df_len = len(df)
    if df_len == 0:
        return df
    if p_id == None:
        print(f"{taxa} total: {df_len}")
    else:
        print(f"{taxa}_{p_id} total: {df_len}")

    host = "ftp.ncbi.nlm.nih.gov"
    ftp_con = FTPConnection()
    ftp_con.set_host(host)
    ftp_con.connect()

    df["is_downloaded"] = df.apply(lambda row: data_download(
        row, ftp_con, taxa, p_id, df_len), axis=1)

    ftp_con.close()

    # create_data_file("tsv", df, taxa, p_id)
    return df


if __name__ == '__main__':
    taxa_list = ["archaea", "fungi", "viral", "protozoa", "bacteria"]
    for taxa in taxa_list:
        df = download_summary(taxa)
        df = modify_taxa_meta(df, taxa)
        df = check_is_downloaded(df, taxa)
        df = download_taxa_data(df)
        break
