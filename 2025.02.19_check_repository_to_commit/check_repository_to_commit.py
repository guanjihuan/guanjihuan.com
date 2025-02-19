import guan

# 在某个目录中寻找所有 Git 项目
git_repository_array = guan.find_git_repositories('D:/')
guan.print_array(git_repository_array)
print('\n---\n')

# 获取未 git commit 的 Git 项目
git_repository_array_to_commit = guan.get_git_repositories_to_commit(git_repository_array)
guan.print_array(git_repository_array_to_commit)
print('\n---\n')

import os

# 完成 git commit
for directory in git_repository_array_to_commit:
    print(directory)
    os.chdir(directory)  # 进入 Git 仓库
    os.system('git add .') # 添加文件到暂存区
    os.system('git commit -m update')  # 将暂存区内容添加到仓库中