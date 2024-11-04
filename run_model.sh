#!/bin/bash
DIR="logs/debug_logs"

# 检查目录是否存在
if [ ! -d "$DIR" ]; then
  # 如果目录不存在，则创建目录
  mkdir -p "$DIR"
  echo "Directory $DIR created."
else
  echo "Directory $DIR already exists."
fi

nohup python -u qanything_kernel/dependent_server/rerank_server/rerank_server.py --use_gpu > logs/debug_logs/rerank_server.log 2>&1 &
PID1=$!
# nohup python -u qanything_kernel/dependent_server/embedding_server/embedding_server.py --use_gpu --workers 1 > logs/debug_logs/embedding_server.log 2>&1 &
# PID2=$!
# 生成close.sh脚本，写入kill命令
echo "#!/bin/bash" > close.sh
echo "kill $PID1" >> close.sh
echo "rm -rf logs" >> close.sh
chmod +x close.sh
