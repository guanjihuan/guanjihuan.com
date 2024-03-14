import guan
file_list_60 = guan.get_all_filenames_in_directory(directory='./2018_01_01_to_2024_03_07/stock_data_60', \
                                        file_format=None, show_root_path=0, sort=1, include_subdirectory=1)
file_list_00 = guan.get_all_filenames_in_directory(directory='./2018_01_01_to_2024_03_07/stock_data_00', \
                                        file_format=None, show_root_path=0, sort=1, include_subdirectory=1)
# print(len(file_list_60))
# print(len(file_list_00))
# print()

# 回测策略：当跌到成本时的 ratio 倍时，翻倍投入补仓。（这里只对00开头的股票进行回测）
buy_limit = 100
for buy_limit in [100000, 10, 4]: # 限制补仓次数
    print('限制补仓次数：', buy_limit, '\n')
    for ratio in [0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65]:
        win_count = 0
        lose_count = 0
        win_count_relative = 0
        lose_count_relative = 0
        win_count_0 = 0
        lose_count_0 = 0
        print('跌到成本的某个倍数补仓：', ratio)
        invest_money_array = []
        current_money_array = []
        buy_times_array = []
        profit_array = []
        profit_array_0 = []
        for i00 in range(len(file_list_00)):
            stock_data = guan.load_data('./2018_01_01_to_2024_03_07/stock_data_00/'+file_list_00[i00], file_format='')
            stock_data = stock_data[::-1]
            if len(stock_data) > 0:
                invest_money = 1000  # 初始投入资金
                current_money = 1000  # 当前所有资金
                buy_price = stock_data[0, 2]  # 买入的价格（第一天买入）
                cost_price = stock_data[0, 2]  # 当前持有的成本价（第一天买入）
                cost_num = invest_money/cost_price   # 当前持有的股数（为了简化，这里不做取整处理）
                len_date = len(stock_data[:, 2])
                buy_times = 0
                for i0 in range(len_date):
                    if stock_data[i0, 2]/cost_price < ratio and buy_times < buy_limit:  # 当满足策略，且补仓次数小于buy_limit时，补仓
                        current_price = stock_data[i0, 2]   # 当前的市场价
                        current_money = invest_money + (invest_money/cost_price)*current_price  # 补仓后的所有资金
                        buy_price = stock_data[i0, 2]  # 买入价为当前市场价
                        cost_num = (invest_money/cost_price)+(invest_money/buy_price)  # 更新当前持有的股数
                        cost_price = 2*invest_money/cost_num # 更新当前持有的成本价
                        invest_money = invest_money*2  # 更新总投入资金
                        buy_times += 1
                    current_price = stock_data[i0, 2]   # 当前的市场价
                    current_money = cost_num*current_price # 当前所有资金 
                buy_times_array.append(buy_times)
                invest_money_array.append(invest_money)
                current_money_array.append(current_money)
                profit_array.append(current_money/invest_money)
                profit_array_0.append(current_price/stock_data[0, 2])
                if current_money > invest_money:
                    win_count += 1
                else:
                    lose_count += 1
                if current_money/invest_money > current_price/stock_data[0, 2]:
                    win_count_relative += 1
                else:
                    lose_count_relative += 1
                if current_price > stock_data[0, 2]:
                    win_count_0 += 1
                else:
                    lose_count_0 += 1
        print('策略的平均加仓次数：', sum(buy_times_array)/len(buy_times_array))
        print('策略的平均投入资金：', sum(invest_money_array)/len(invest_money_array))
        print('策略的平均最终所有资金：', sum(invest_money_array)/len(invest_money_array))
        print('策略的平均利润率（包含本金）：', sum(profit_array)/len(profit_array))
        print('完成不操作的市场平均利润率（包含本金）：', sum(profit_array_0)/len(profit_array_0))
        print('策略赢的次数：', win_count)
        print('策略输的次数；', lose_count)
        print('策略相对于市场赢的次数：', win_count_relative)
        print('策略相对于市场输的次数；', lose_count_relative)
        print('完全不操作市场赢的次数：', win_count_0)
        print('完全不操作市场输的次数；', lose_count_0)
        print()
    print('-----')
    print()