import pandas as pd
from pathlib import Path
from datetime import datetime


def create_excel(metrics, trades, equity_chart, start, end):

    summary_data = {

        "Report Created":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "Reporting Period":
            f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}",

        **metrics

    }


    summary_df = pd.DataFrame(
        summary_data.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


    output_dir = Path("reports/excel")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    filename = (
        f"{start.strftime('%Y-%m-%d')}_to_{end.strftime('%Y-%m-%d')}_MT5_Analysis_Report.xlsx"
    )


    with pd.ExcelWriter(
        output_dir / filename
    ) as writer:


        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )


        trades.to_excel(
            writer,
            sheet_name="Trades",
            index=False
        )