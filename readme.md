# MT5 Automated Reporting

A Python tool that connects to a MetaTrader 5 (MT5) account, pulls trade and account history, calculates performance and risk metrics, and generates a formatted Excel report — complete with an equity curve chart.

## Features

- **Automatic MT5 connection** using saved credentials or an interactive prompt
- **Configurable reporting period** — custom date range, or defaults to a rolling 3-year history
- **Performance analytics** — initial capital, total trades, net P/L, net P/L %, win rate
- **Risk metrics** — average P/L per trade, final portfolio value
- **Equity curve chart** generated with Plotly
- **Excel report output** with Summary and Trades sheets, automatically saved with the reporting period in the filename
- **Optional standalone executable** build via PyInstaller (no Python/IDE required to run)

## Requirements

- Windows (required by the `MetaTrader5` Python package)
- Python 3.10+
- An MT5 terminal installed and a trading account (demo or live)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository.
2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the project root:

```
python main.py
```

You'll be prompted for:

1. **MT5 login credentials** — account number, password, and server (only if `config.py` doesn't already exist; see [Configuration](#configuration) below). Optionally save these for future runs.
2. **Reporting period** — a start and end date (`YYYY-MM-DD`), or leave both blank to default to the last 3 years.

The tool will then:

1. Connect to MT5
2. Extract trade and account history (a full 3-year history for capital/risk detection, plus the chosen reporting period for trade-level analysis)
3. Clean and transform the raw deal data into a trade log
4. Calculate performance and risk metrics
5. Generate an equity curve chart
6. Write an Excel report to `reports/excel/`
7. Disconnect from MT5

## Configuration

Credentials can be provided two ways:

- **`config.py`** in the project root (auto-detected if present):
  ```python
  account_id = 12345678
  password = "your_password"
  server = "YourBroker-Server"
  ```
- **Interactive prompt** — if `config.py` isn't found, you'll be asked to enter your account number, password, and server (defaults to `MetaQuotes-Demo` if left blank). You can choose to save these to `config.py` for next time.

> **Note:** `config.py` contains plaintext credentials and should never be committed to version control. Make sure it's listed in `.gitignore`.
>
> **Note:** Password input in the terminal is currently visible as you type (not masked), since `getpass`-based hidden input proved unreliable across some terminal environments. Only run this in a private, secure environment.

## Output

Reports are saved to:

```
reports/excel/{start_date}_to_{end_date}_MT5_Analysis_Report.xlsx
```

If the /reports folder does not exist it will be created automatically. 

Each report contains:

- **Summary sheet** — report creation time, reporting period, and all calculated performance/risk metrics
- **Trades sheet** — the full list of completed trades for the reporting period

## Project Structure

```
.
├── main.py                 # Entry point — orchestrates the full pipeline
├── config.py                # (optional, gitignored) saved MT5 credentials
├── requirements.txt
└── src/
    ├── setup_config.py     # Loads or prompts for MT5 credentials
    ├── setup_dates.py      # Prompts for / defaults the reporting period
    ├── mt5_client.py        # Handles MT5 connect/disconnect
    ├── extract.py           # Pulls raw trade & account data from MT5
    ├── transform.py         # Cleans raw deals into a usable trade log
    ├── analytics.py         # Performance metrics (P/L, win rate, etc.)
    ├── risk.py               # Risk metrics (average P/L, final portfolio value)
    ├── charts.py             # Equity curve chart generation
    └── report_excel.py      # Builds and saves the final Excel report
```

## Building a Standalone Executable

To run this without needing Python or an IDE installed:

```
pip install pyinstaller
pyinstaller --onefile --console main.py
```

The executable will be created at `dist/main.exe`. Run it from a folder where `config.py` can also live alongside it (or use the interactive credential prompt on first run).

## .gitignore

Recommended entries:

```
.venv/
__pycache__/
*.pyc
build/ # If pyinstaller is ran
dist/ # If pyinstaller is ran
*.spec
config.py
reports/
```