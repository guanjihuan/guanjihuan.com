import guan

# 当前目录所在的 Git 项目中 git commit 次数的每日统计
date_array, commit_count_array = guan.statistics_of_git_commits()

# 获取某个月份的日期
date_array_of_month = guan.get_date_array_of_the_current_month() # 本月
# date_array_of_month = guan.get_date_array_of_the_last_month() # 上个月
# date_array_of_month = guan.get_date_array_of_the_month_before_last() ## 上上个月

# 根据某个月份的日期，对原统计数据的进行处理
new_commit_count_array = guan.fill_zero_data_for_new_dates(old_dates=date_array, new_dates=date_array_of_month, old_data_array = commit_count_array)

# 画图
plt, fig, ax = guan.import_plt_and_start_fig_ax(adjust_bottom=0.28, adjust_left=0.2, labelsize=10, fontfamily='Times New Roman')
plt.xticks(rotation=90)  # 旋转横轴刻度标签
guan.plot_without_starting_fig_ax(plt, fig, ax, date_array_of_month, new_commit_count_array, style='o-', xlabel='date', ylabel='commits', fontsize=25)
plt.show()