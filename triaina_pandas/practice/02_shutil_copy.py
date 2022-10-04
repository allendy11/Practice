'''
Created on Sep 29, 2022

@author: neuroears
'''
import os, glob, shutil
from tqdm import tqdm

if __name__ == '__main__':
    # list = ['a','b','c','d']
    # for ch in tqdm(list):
    #     print(ch)
    
    # for i in tqdm(range(100), desc='Processing', mininterval=0.0001):
    #     print('\n')
    #     print(i)
    
    # pb = tqdm(range(100), desc='Processing', mininterval=0.00001)
    # for i in pb:
    #     print(i)
    
    # with tqdm(tatal=100) as pbar:
    #     for i in range(10):
    #         print(i)
    #         pbar.update(10)
    
    # pb = tqdm(total=100, desc='Processing')
    # for i in range(10):
    #     print(i)
    #     pb.update(10)
    # pb.close()
    
    cwd = os.getcwd()
    hospital = 'SCHBC'
    tsv_list = glob.glob(f'{cwd}/{hospital}/**/*.tsv', recursive=True)
    # for tsv_file in tsv_list:
    #     print(tsv_file)
    # for tsv_file in tqdm(tsv_list, mininterval=0.00001):
    n=len(tsv_list)
    for i,tsv_file in tqdm(enumerate(tsv_list), mininterval=0.00001):
        print(int(i/n*100))
    # for tsv_file in tsv_list:
        new_tsv_file = tsv_file.replace('SCHBC', 'BUSAN')
        new_tsv_path = os.path.dirname(new_tsv_file)
        
        print(new_tsv_file)
        print(new_tsv_path)
        # print(os.path.isfile(new_tsv_file))
        # print(os.path.isdir(new_tsv_path))
        
        if not os.path.isdir(new_tsv_path):
            os.makedirs(new_tsv_path)
        if not new_tsv_file in os.listdir(new_tsv_path):
            shutil.copy(tsv_file, new_tsv_file)
        # break
    