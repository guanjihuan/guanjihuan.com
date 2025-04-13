goto() {
    # 获取作业的工作目录
    workdir=$(scontrol show job "$1" | grep WorkDir | awk -F= '{print $2}')
    # 检查路径是否存在
    if [ -d "$workdir" ]; then
        cd "$workdir" && echo "已跳转到作业 $1 的工作目录: $workdir"
    else
        echo "错误：无法定位作业 $1 的工作目录" >&2
        return 1
    fi
}

alias wdir="scontrol show job | grep WorkDir | awk -F= '{print $2}'"
