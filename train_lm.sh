#!/bin/bash
#     --validation_file lm_data_mimic_stroke/val_file.txt \
python run_clm.py \
    --model_name lm_outputs_mimic \
    --use_fast_tokenizer \
    --output_dir lm_mimic_kch_test \
    --cache_dir hf_cache \
    --block_size 512 \
    --save_steps 1000 \
    --save_total_limit 2 \
    --train_file wikiText2-test.txt \
    --validation_file kch_stroke_data/test_file.txt \
    --do_eval \
    --evaluation_strategy epoch \
    --preprocessing_num_workers 45 \
    --per_device_train_batch_size 6 \
    --per_device_eval_batch_size 6 \
    --gradient_accumulation_steps 1 \
    --warmup_steps 100 \
    --weight_decay 0.01 \
    --num_train_epochs 8 \
    --ignore_data_skip 
    
