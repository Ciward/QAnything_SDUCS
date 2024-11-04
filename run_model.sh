#!/bin/bash
nohup python -u qanything_kernel/dependent_server/rerank_server/rerank_server.py > ../logs/debug_logs/rerank_server.log 2>&1 &
PID1=$!
nohup python -u qanything_kernel/dependent_server/embedding_server/embedding_server.py > ../logs/debug_logs/embedding_server.log 2>&1 &
PID2=$!
# 生成close.sh脚本，写入kill命令
echo "#!/bin/bash" > close.sh
echo "kill $PID1 $PID2" >> close.sh
