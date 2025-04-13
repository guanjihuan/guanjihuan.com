goto() {
    # 获取作业的工作目录
    workdir=$(qstat -f "$1" | grep init_work_dir | awk '{print $3}')
    # 检查路径是否存在
    if [ -d "$workdir" ]; then
        cd "$workdir" && echo "已跳转到作业 $1 的工作目录: $workdir"
    else
        echo "错误：无法定位作业 $1 的工作目录" >&2
        return 1
    fi
}

alias wdir="qstat -f | grep init_work_dir | awk '{print $3}'"

alias wdir_jhguan="qstat -u jhguan -f | grep init_work_dir | awk '{print $3}'"
