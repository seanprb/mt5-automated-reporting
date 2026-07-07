import pandas as pd

def create_trade_log(df):

    if df.empty:
        print("No trades available to create log")
        return pd.DataFrame()

    if "position_id" not in df.columns:
        raise ValueError(
            "position_id missing. Cannot combine trades."
        )

    trades = []


    df = df[
        df["Position"] != "CAPITAL"
    ]


    for position_id, group in df.groupby("position_id"):

        entry = group[
            group["entry"] == 0
        ]

        exit = group[
            group["entry"] == 1
        ]


        if entry.empty or exit.empty:
            continue


        trade = {

            "Date": exit["Date"].iloc[0],

            "Ticker": exit["Ticker"].iloc[0],

            "Position":
                "BUY"
                if entry["type"].iloc[0] == 0
                else "SELL",

            "Lot":
                entry["Lot"].iloc[0],

            "Entry Point ($)":
                entry["Entry Point ($)"].iloc[0],

            "Exit Point ($)":
                exit["Entry Point ($)"].iloc[0],

            "Actual P/L ($)":
                exit["Actual P/L ($)"].iloc[0]
        }


        trades.append(trade)


    return pd.DataFrame(
        trades,
        columns=[
            "Date",
            "Ticker",
            "Position",
            "Lot",
            "Entry Point ($)",
            "Exit Point ($)",
            "Actual P/L ($)"
        ]
    )


def clean_trades(df):

    if df.empty:
        print("No trades to transform")
        return pd.DataFrame(
            columns=list(df.columns) + ["Date", "Position"]
        )


    # Rename MT5 columns
    df = df.rename(
        columns={
            "volume": "Lot",
            "price": "Entry Point ($)",
            "profit": "Actual P/L ($)",
            "symbol": "Ticker"
        }
    )


    # Convert timestamp
    df["Date"] = pd.to_datetime(
        df["time"],
        unit="s"
    )


    # Create Position
    df["Position"] = df["type"].map(
        {
            0: "BUY",
            1: "SELL",
            2: "CAPITAL"
        }
    )


    return df
