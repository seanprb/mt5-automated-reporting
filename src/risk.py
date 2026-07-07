class RiskManager:


    def __init__(self, trades):

        self.trades = trades



    def initial_capital(self):

        capital = self.trades[
            self.trades["Position"] == "CAPITAL"
        ]


        if capital.empty:
            return 0


        return (
            capital["Actual P/L ($)"]
            .iloc[0]
        )



    def trade_data(self):

        return self.trades[
            self.trades["Position"]
            !=
            "CAPITAL"
        ]



    def average_pl(self):

        trades = self.trade_data()


        if trades.empty:

            return 0


        return (
            trades["Actual P/L ($)"]
            .mean()
        )



    def final_portfolio_value(self):

        trades = self.trade_data()

        total_pl = (
            trades["Actual P/L ($)"].sum()
            if not trades.empty
            else 0
        )

        return (
            self.initial_capital()
            + total_pl
        )


    def summary(self):

        return {

            "Average P/L":
                self.average_pl(),

            "Final Portfolio Value":
                self.final_portfolio_value()

        }