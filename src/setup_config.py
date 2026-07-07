from types import SimpleNamespace


def load_credentials():

    try:
        import config

        return SimpleNamespace(
            account_id=config.account_id,
            password=config.password,
            server=getattr(config, "server", None) or "MetaQuotes-Demo"
        )

    except ModuleNotFoundError:

        print(
            "No config.py found — enter your MT5 account details "
            "(Note: Password will be visible on input, please ensure "
            "your environment is secure)."
        )

        account_id = input("Account number: ").strip()

        password = input("Password: ")

        server = input(
            "Server (leave blank to use MetaQuotes-Demo): "
        ).strip()

        server = server or "MetaQuotes-Demo"

        save = input(
            "Save these login details for next time? (Y/N): "
        ).strip().upper()

        if save == "Y":
            _save_config(account_id, password, server)

        return SimpleNamespace(
            account_id=int(account_id),
            password=password,
            server=server
        )


def _save_config(account_id, password, server):

    content = (
        f"account_id = {int(account_id)}\n"
        f"password = {password!r}\n"
        f"server = {server!r}\n"
    )

    with open("config.py", "w") as f:
        f.write(content)

    print("Saved to config.py.")