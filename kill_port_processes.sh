#!/bin/bash

# 檢查是否有傳入端口號作為參數
if [ -z "$1" ]; then
    echo "Usage: $0 <port>"
    exit 1
fi

# 讀取第一個命令行參數作為端口
PORT=$1

# 使用 lsof 指令來查找佔用指定端口的所有 PID
PIDS=$(lsof -ti :$PORT)

# 檢查是否找到任何 PID
if [ -z "$PIDS" ]; then
    echo "No processes are using port $PORT."
else
    echo "Killing the following processes using port $PORT: $PIDS"
    # 循環遍歷每個 PID 並強制終止這些進程
    for PID in $PIDS; do
        kill -9 $PID
    done
    echo "Processes killed."
fi
