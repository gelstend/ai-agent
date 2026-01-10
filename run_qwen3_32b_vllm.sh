#!/usr/bin/env bash
set -e

MODEL_PATH="/root/Qwen3-32B"
LOG_DIR="/root/model_train"
LOG_FILE="$LOG_DIR/qwen3_32b.log"

mkdir -p $LOG_DIR

nohup vllm serve $MODEL_PATH \
  --model Qwen3-32B \
  --max-model-len 16384 \
  --gpu-memory-utilization 0.95 \
  --host 0.0.0.0 \
  --port 8000 \
  > $LOG_FILE 2>&1 &

echo "Qwen3-32B vLLM 已启动"
echo "日志: $LOG_FILE"
echo "API: http://0.0.0.0:8000"
