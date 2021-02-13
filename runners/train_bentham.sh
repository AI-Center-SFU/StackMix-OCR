# if you need resume experiment, should set checkpoint_path
python scripts/run_train.py --experiment_name debug \
  --checkpoint_path "" \
  --experiment_name "bentham_base" \
  --dataset "bentham" \
  --data_dir "../StackMix-OCR-DATA" \
  --output_dir "../StackMix-OCR-SAVED_MODELS" \
  --experiment_description "[Base] Training OCR on Bentham dataset" \
  --image_w 2048 \
  --image_h 128 \
  --num_epochs 150 \
  --bs 16 \
  --num_workers 4 \
  --use_blot 0 \
  --use_progress_bar 0 \
  --neptune_project "" \
  --neptune_token "" \
  --seed 6955
