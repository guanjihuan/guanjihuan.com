mkpbs() {
  # 参数说明：mkpbs [文件名] [作业名] [节点数] [核心/节点] [Python文件]
  # 默认值
  FILENAME="${1:-task.sh}"  # 第一个参数：文件名（默认 task.sh）
  JOB_NAME="${2:-task}"       # 第二个参数：作业名（默认 task）
  NODES="${3:-1}"            # 第三个参数：节点数（默认 1）
  PPN="${4:-1}"              # 第四个参数：每节点核心数（默认 1）
  PYTHON_FILE="${5:-a.py}"   # 第五个参数：Python 文件（默认 a.py）

  # 生成 PBS 脚本
  cat << EOF > "$FILENAME"
#!/bin/sh
#PBS -N $JOB_NAME
#PBS -l nodes=$NODES:ppn=$PPN
python $PYTHON_FILE
EOF

  echo "已生成文件：$FILENAME"
  echo "├─ 作业名：$JOB_NAME"
  echo "├─ 节点数：$NODES"
  echo "├─ 核心/节点：$PPN"
  echo "└─ 执行文件：$PYTHON_FILE"
}