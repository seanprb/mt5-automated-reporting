import MetaTrader5 as mt5


class MT5Client:


    def __init__(
        self,
        login,
        password,
        server
    ):

        self.login = login
        self.password = password
        self.server = server



    def connect(self):

        if not mt5.initialize(
            login=self.login,
            password=self.password,
            server=self.server
        ):

            raise RuntimeError(
                "Failed to connect to MT5"
            )


        print(
            "Connected to MT5"
        )



    def disconnect(self):

        mt5.shutdown()

        print(
            "Disconnected from MT5"
        )