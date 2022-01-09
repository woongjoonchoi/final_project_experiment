python train_copy.py --output_dir ./outputs  --run_extraction True --run_generation False --do_train --do_eval \
--evaluation_strategy 'steps' --eval_steps 60 --logging_steps 60 --per_device_eval_batch_size 16 \
 --per_device_train_batch_size 16 --save_strategy "no" --fp16 True --fp16_full_eval True --num_train_epochs 9 --report_to "wandb" \
 --overwrite_output_dir
