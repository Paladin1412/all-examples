#!/bin/bash

# 配置要启动关闭的脚本名
process_name="run_spider.py"

# 添加启动命令
function start(){
    echo "start..."

    nohup python3 $process_name 2>&1 &

    echo "start successful"
    return 0
}

# 添加停止命令
function stop(){
    echo "stop..."

    ps aux |grep $process_name |grep -v grep |awk '{print "kill -9 " $2}'|sh

    echo "stop successful"
    return 0
}

case $1 in
"start")
    start
    ;;
"stop")
    stop
    ;;
"restart")
    stop && start
    ;;
*)
    echo "请输入: start, stop, restart"
    ;;
esac