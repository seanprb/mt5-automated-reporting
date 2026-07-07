import pandas as pd


class PerformanceAnalytics:


    def __init__(self, trades, account_history):
        self.trades = trades              # completed trade log
        self.account_history = account_history  # raw deals incl. CAPITAL

    def initial_capital(self):
        capital = self.account_history[
            self.account_history["Position"] == "CAPITAL"
        ]
        if capital.empty:
            return 0
        return capital["Actual P/L ($)"].iloc[0]

    def trade_data(self):

        return self.trades[
            self.trades["Position"] != "CAPITAL"
        ]


    def total_profit(self):

        trades = self.trade_data()

        if trades.empty:
            return 0


        return (
            trades["Actual P/L ($)"]
            .sum()
        )


    def win_rate(self):

        trades = self.trade_data()

        if trades.empty:
            return 0


        wins = trades[
            trades["Actual P/L ($)"] > 0
        ]


        return (
            len(wins)
            /
            len(self.trade_data())
            *
            100
        )
        
    def net_profit_percentage(self):

        capital = self.initial_capital()


        if capital == 0:

            return 0


        return (
            self.total_profit()
            /
            capital
            *
            100
        )



    def summary(self):

        return {

            "Initial Capital":
                self.initial_capital(),

            "Total Trades":
                len(self.trade_data()),

            "Net Profit/Loss":
                self.total_profit(),

            "Net Profit/Loss %":
                self.net_profit_percentage(),

            "Win Rate":
                self.win_rate()

        }