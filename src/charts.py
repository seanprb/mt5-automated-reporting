import plotly.express as px


def equity_curve(df):

    if (
        df.empty
        or "Actual P/L ($)" not in df.columns
    ):
        print("No trades available for equity chart")
        return None


    df = df.copy()


    df["Equity"] = (
        df["Actual P/L ($)"]
        .cumsum()
    )


    fig = px.line(
        df,
        x="Date",
        y="Equity",
        title="Equity Curve"
    )


    return fig