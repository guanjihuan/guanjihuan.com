"""
This code is supported by the website: https://www.guanjihuan.com
The newest version of this code is on the web page: https://www.guanjihuan.com/archives/706
"""

import numpy as np
import time
import matplotlib.pyplot as plt
import tushare as ts


def main():
    start_clock = time.perf_counter()
    pro = ts.pro_api('到官网上注册，寻找Token填在这里!')
    print('\n我的策略：见好就收，遇低抄底。\n'
          '   【卖出】买入后涨了5%就卖出\n'
          '   【买入】卖出后跌了5%就买入\n'
          '注：第一天必须买进，最后一天前必须卖出(为了与不操作的做对比)\n')
    number = 1
    for i in range(number):
        data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')   # 所有股票列表
        # print(data.columns)  # 查看该数据的表头
        # print(data)  # 3688多行的股票数据
        i = 1  # 查看第二行数据“万科A”股
        ts_code = data.values[i, 0]  # 股票代码
        stock = data.values[i, 2]  # 股票名称
        industry = data.values[i, 4]  # 属于哪个行业
        start_date = '20110101'  # 开始时间
        end_date = '20191027'  # 结束时间
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)  # 查看该股票的日线数据
        # print(df.columns)  # 查看该数据的表头
        # print(df)  # 查看该股票的日线数据
        close = np.array(list(reversed(df.values[:, 5])))  # 提取出收盘价，并按时间顺序排列，从过去到现在
        pct_chg = np.array(list(reversed(df.values[:, 8])))  # 提取出涨跌幅，并按时间顺序排列，从过去到现在
        # print(df.columns[5], '=', close, '\n')  # 查看收盘价
        # print(df.columns[8], '=', pct_chg, '\n')  # 查看涨跌幅
        profit, profit_no_operation, times, invest_money, buy_time_all, sell_time_all = back_test(close.shape[0], close, pct_chg)
        # 调用回测函数，返回了“利润，未操作的利润， 按该策略操作了几次， 总投资金额， 按该策略买的时间， 按该策略卖的时间”的值
        print('\n------股票：', stock, ts_code, industry, '[买入市值=%7.2f' % invest_money, ']------')
        print('回测时间段：', start_date, '-', end_date)
        print('操作后利润= %6.2f' % profit, '  买入（卖出）次数=', times, ' ')
        print('不操作利润= %6.2f' % profit_no_operation, '（第一天买入，最后一天卖出，中间未操作）')
    end_clock = time.perf_counter()
    print('CPU执行时间=', end_clock - start_clock, 's')
    plt.figure(1)
    plt.title('Stock Code: '+ts_code+'  (red point: buy,  green point: sell)')
    plt.grid()
    plt.plot(range(close.shape[0]), close, '-')
    for i in buy_time_all:
        plt.plot(i, close[int(i)], 'or', markersize=13)  # 红色是买进的点
    for i in sell_time_all:
        plt.plot(i, close[int(i)], 'dg', markersize=13)  # 绿色是卖出的点
    plt.show()


def back_test(days, close, pct_chg, money_in=10000):  # 定义该策略的回测效果（按旧数据检查该策略是否有效）
    money_in_amount = int(money_in/close[0])  # 投资金额换算成股票股数
    invest_money = close[0]*money_in_amount  # 实际买了股票的金额
    profit_no_operation = (close[close.shape[0]-1]-close[0])*money_in_amount  # 不操作的利润
    position = -1  # 买入还是卖出的状态，默认卖出
    total_profit = 0
    times = 0
    current_buy_pct = -999
    current_sell_pct = 999
    buy_time_all = np.array([])
    sell_time_all = np.array([])
    for i in range(days):  # 总天数
        if i == 0:  # 第一天，满仓买买买！为了和不操作的对比，第一天就要买入。
            buy_time = i  # 买入时间
            buy_time_all = np.append(buy_time_all, [buy_time], axis=0)  # 买入时间存档
            position = 1  # 标记为买入状态
            print('------------------第', buy_time, '天买进-------------')
        else:
            profit = 0
            if position == 1:  # 买入状态
                current_buy_pct = (close[i]-close[buy_time])/close[buy_time]*100  # 买入后的涨跌情况
                # print('当前买进后的涨跌情况：第', i, '天=', current_buy_pct)
            if position == 0:  # 卖出状态
                current_sell_pct = (close[i]-close[sell_time])/close[sell_time]*100  # 卖出后的涨跌情况

            if current_sell_pct < -5 and position == 0:  # 卖出状态，且卖出后跌了有3%，这时候买入
                buy_time = i  # 买入时间
                buy_time_all = np.append(buy_time_all, [buy_time], axis=0)  # 买入时间存档
                print('------------------第', buy_time, '天买进-------------')
                position = 1  # 标记为买入状态
                continue

            if current_buy_pct > 5 and position == 1:  # 买入状态，且买入后涨了有3%，这时候卖出
                sell_time = i  # 卖出时间
                sell_time_all = np.append(sell_time_all, [sell_time], axis=0)  # 卖出时间存档
                print('----------第', sell_time, '天卖出，持有天数：', sell_time-buy_time, '--------------\n')
                position = 0  # 标记为卖出状态
                profit = close[sell_time]-close[buy_time]  # 赚取利润
                times = times + 1  # 买入（卖出）次数加1
            total_profit = total_profit + profit*money_in_amount  # 计算总利润
    if position == 1:  # 最后一天如果是买入状态，则卖出
        profit = close[i]-close[buy_time]  # 赚取利润
        total_profit = total_profit + profit  # 计算总利润
        times = times + 1  # 买入（卖出）次数加1
        print('--------------第', i, '天（最后一天）卖出，持有天数：', sell_time-buy_time, '--------------\n')
        sell_time_all = np.append(sell_time_all, [i], axis=0)  # 卖出时间存档
    return total_profit, profit_no_operation, times, invest_money, buy_time_all, sell_time_all


if __name__ == '__main__':
    main()
