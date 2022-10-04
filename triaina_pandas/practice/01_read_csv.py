'''
Created on Sep 29, 2022

@author: neuroears
'''

import os
import glob
import pandas as pd
from email.policy import default

def fun(main_dir):
    output=list()
    for i in os.listdir(main_dir):
        output.append(f'{main_dir}/{i}')
    return output

def getOpenEyes(main_dir):
    tsv_list = glob.glob(main_dir + '/*.tsv', recursive=True)
    # print(tsv_list)
    df = pd.read_csv(tsv_list[0], sep='\t')
    # print(df)
    # print(df[0]) # error
    # print(df['blink']) # df[column]
    # print(df['time_sec', 'blink']) # error
    # print(df[['time_sec', 'blink']]) # df[list]
    # print(df['time_sec':'blink']) # error
    # print(df[10:21]) # df[list-slicing]
    
    # print(df.loc[5:10,['time_sec','blink']]) # df.loc[row, column]
    # print(df.loc[[1,5,25,67,83],['time_sec','blink']])
    # print(df.loc[10:20,'time_sec':'blink'])
    
    # print(df.iloc[[1,3,12,52],[1,2,4]])
    # print(df.iloc[10:21,1:5])
    
    # print(df.dtypes)
    # print(df.astype({'frame_number': 'float'}))
    # print((df.iloc[:,4] == 'O').astype('int'))
    print(df.loc[(df.iloc[:,4] == 'O').astype('int') == 1,:])
    
    # print((df.iloc[:,4] == 'O').astype('int').cumsum())
    # print((df.iloc[:,4]).dtypes)
    # print((df.iloc[:,4] == 'O').astype('int'))
    # cumsum_idx = (df.iloc[:4] == '0').astype('int').cumsum()
    # print(cumsum_idx)
    
if __name__ == '__main__':
    # default_path = '/home/neuroears/eclipse-workspace/python/Practice_python/SCHBC'
    # file_list = os.listdir(default_path)
    # # print(path_list)
    # for file in file_list:
    #     # print(file)
    #     path = f'{default_path}/{file}'
    #     # print(os.path.isdir(path))
    #     if os.path.isdir(path):
    #         print(path)
    
    # for list in path_list:
    #     print(list)
    
    # main_dir=os.getcwd()
    
    # path = fun(main_dir)
    
    # for i in path:
    #     print(i)
    
    getOpenEyes(main_dir)