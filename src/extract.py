import MetaTrader5 as mt5
import pandas as pd

def get_account_info():

    account = mt5.account_info()


    if account is None:

        return {}


    return {

        "balance": account.balance,

        "equity": account.equity,

        "margin": account.margin,

        "free_margin": account.margin_free,

        "profit": account.profit

    }

def get_trades(start, end):

    raw = mt5.history_deals_get(
        start,
        end
    )


    if raw is None or len(raw) == 0:

        print("No trades found for this period")

        return pd.DataFrame(
            columns=[
                "ticket",
                "order",
                "time",
                "time_msc",
                "type",
                "entry",
                "magic",
                "position_id",
                "reason",
                "Lot",
                "Entry Point ($)",
                "commission",
                "swap",
                "Actual P/L ($)",
                "fee",
                "Ticker",
                "comment",
                "external_id"
            ]
        )


    df = pd.DataFrame(
        list(raw),
        columns=raw[0]._asdict().keys()
    )

    return df