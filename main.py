from datetime import timedelta, datetime
import MetaTrader5 as mt5

from src.setup_config import load_credentials
from src.setup_dates import get_reporting_period
from src.mt5_client import MT5Client
from src.extract import get_trades, get_account_info
from src.transform import clean_trades, create_trade_log
from src.analytics import PerformanceAnalytics
from src.risk import RiskManager
from src.charts import equity_curve
from src.report_excel import create_excel


def main():

    print("Starting MT5 Trading Analytics...")

    # -------------------------
    # 1. Connect to MT5
    # -------------------------

    creds = load_credentials()

    client = MT5Client(
        login=creds.account_id,
        password=creds.password,
        server=getattr(creds, "server", None)
    )

    client.connect()

    try:

        # -------------------------
        # 2. Define reporting period
        # -------------------------

        start, end = get_reporting_period()

        # -------------------------
        # 3. Extract data
        # -------------------------

        print("Extracting trades...")

        # Full history — always scanned for CAPITAL (type 2) rows,
        # independent of the reporting window the user chose
        full_history = get_trades(
            datetime.now() - timedelta(days=365 * 3),
            datetime.now() + timedelta(days=1)
        )

        account_history = clean_trades(
            full_history
        )

        print("Full history rows:", len(full_history))
        print("MT5 last error:", mt5.last_error())

        # Report-period trades only
        trades = get_trades(
            start,
            end
        )

        # -------------------------
        # 4. Transform data
        # -------------------------

        print("Cleaning data...")

        trades = clean_trades(
            trades
        )

        print("Creating trade log...")

        trades = create_trade_log(
            trades
        )

        # -------------------------
        # 5. Analytics
        # -------------------------

        print("Calculating performance...")

        analytics = PerformanceAnalytics(
            trades,
            account_history
        )

        metrics = analytics.summary()

        # -------------------------
        # 6. Risk analysis
        # -------------------------

        print("Checking risk...")

        risk_manager = RiskManager(
            account_history
        )

        risk_metrics = (
            risk_manager.summary()
        )

        metrics.update(
            risk_metrics
        )

        # -------------------------
        # 7. Generate charts
        # -------------------------

        print("Creating charts...")

        equity_chart = equity_curve(
            trades
        )

        # -------------------------
        # 8. Generate reports
        # -------------------------

        print("Creating Excel report...")

        create_excel(
            metrics,
            trades,
            equity_chart,
            start,
            end
        )

        print(
            "Report generation completed!"
        )

    finally:

        # -------------------------
        # 9. Disconnect MT5
        # -------------------------

        client.disconnect()

        print(
            "MT5 disconnected"
        )


if __name__ == "__main__":

    main()