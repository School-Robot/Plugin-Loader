#!/bin/bash

cnt_failed_running=0 #计数器，当失败次数达到一定程度，则进入bash模式，手动调试
cnt_max_failed_running=10 #最大重试次数
restart_time=5 #自动重启的秒数

trap 'onCtrlC' INT

function entry_bash_maintain(){
  echo -e "\033[31m[School-Bot-Plugin-Loaderdocker]进入shell模式,请通过 \033[36m docker attach School-Bot-Plugin-Loader(School-Bot-Plugin-Loader为容器名) \033[0m 进入容器shell手动维护,结束维护输入\033[36m exit \033[0m \033[0m"
  /bin/bash
  echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]检测到shell模式退出,重置计数器,并且尝试重新启动School-Bot-Plugin-Loader\033[0m"
  cnt_failed_running=0
}

function onCtrlC() {
  echo -e "\033[36m[School-Bot-Plugin-Loaderdocker]检测到Ctrl+C,进入shell模式..\033[0m"
  entry_bash_maintain
}

while :
do
  echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]当前运行目录为(容器内部运行目录): $PWD \033[0m"
  stillRunning=$(ps -ef |grep "python main.py" |grep -v "grep")
  if [ "$stillRunning" ] ; then
    echo -e "\033[31m[School-Bot-Plugin-Loaderdocker]检测到School-Bot-Plugin-Loader已经正在运行\033[0m" 
    echo -e "\033[31m[School-Bot-Plugin-Loaderdocker]避免冲突,正在尝试杀死School-Bot-Plugin-Loader\033[0m" 
    kill -9 $(pidof python)
    stillRunning2=$(ps -ef |grep "python main.py" |grep -v "grep")
    if [ "$stillRunning2" ]  
    then
      echo -e "\033[31m[School-Bot-Plugin-Loaderdocker]进程杀死失败\033[0m"
      echo -e "\033[31m[School-Bot-Plugin-Loaderdocker]也许你应该手动检查下,尝试进入shell模式..."
      entry_bash_maintain
    else
      echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]已经杀死进程\033[0m"
    fi
  else
    echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]School-Bot-Plugin-Loader似乎没有启动,正在尝试启动School-Bot-Plugin-Loader...\033[0m" 
    echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]以下为School-Bot-Plugin-Loader的输出:\033[0m"

    # 执行的命令：
    python main.py
    # 

    echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]以上为School-Bot-Plugin-Loader的输出:\033[0m"
    echo -e "\033[33m[School-Bot-Plugin-Loaderdocker]School-Bot-Plugin-Loader进程退出! \033[0m"

    ((cnt_failed_running=cnt_failed_running+1));

    echo -e "\033[31m[School-Bot-Plugin-Loaderdocker]当前School-Bot-Plugin-Loader运行失败次数为:$cnt_failed_running"
    if [ $cnt_failed_running -gt $cnt_max_failed_running ];
    then
      entry_bash_maintain
    fi
    echo -e "\033[32m[School-Bot-Plugin-Loaderdocker]将会在$restart_time秒后重新尝试启动School-Bot-Plugin-Loader \033[0m"
  fi
  sleep $restart_time
done