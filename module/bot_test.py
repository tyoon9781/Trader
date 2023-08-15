from module.bot import MyBot


def test_main():
    """ test area for bot function """
    
    my_bot = MyBot()
    # my_bot.request_min_info("005930", "20230813")
    # market_list = my_bot.get_kospi_market_info()

    # for market in market_list[1:]:
    #     code = market[0]
    #     dfs_day = my_bot.request_day_history_info(code, "20230813", count=3)
    #     df_day = pd.concat(dfs_day)
    #     df_day.to_excel(f"day/{code}_day.xlsx")

    #     dfs_minute = my_bot.request_minute_history_info(code, "20230813", count=100)
    #     df_minute = pd.concat(dfs_minute)
    #     df_minute.to_excel(f"minute/{code}_minute.xlsx")
    #     print(f"{code} / {market[1]} complete")

    print("Test Done")


if __name__ == "__main__":
    test_main()
