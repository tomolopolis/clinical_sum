from differ import compute_sequential_diff_metrics
import pandas as pd
import numpy as np
import sys
import torch
import os

if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1])
    # break df into blocks of 500 admissions
    print(df.columns)
    adm_ids = df.hadm_id.unique()
    block_size = 500
    df_splits = []
    for block_num in range(int(np.ceil(len(adm_ids) / block_size))):
        block_start = block_num * block_size
        block_end = (block_num+1) * block_size 
        ids = adm_ids[block_num * block_size:block_end if block_end < len(adm_ids) else len(adm_ids)]
        df_splits.append(df[df.hadm_id.isin(ids)])
    
    for i, df in enumerate(df_splits):
        out_file_name = f'kch_rouge_bert_output/df_{i}_diffs.pickle'
        if os.path.exists(out_file_name):
            continue
        df_diffs = compute_sequential_diff_metrics(df)
        df_diffs.to_pickle(out_file_name)
        print(f'Finished block {i}')
    print('Finished!!')
    