__all__ = ["Transaction", "Asset", "Portfolio"]

from typing import List

from pathlib import Path
from loguru import logger
from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import table
from tomlkit import parse
from dataclasses import dataclass, asdict
import datetime
import pandas_datareader as pdr
import pythainav as nav


class SymbolNotFoundError(Exception):
    pass


class GetNAVPriceError(Exception):
    pass


@dataclass
class Transaction:
    """Transaction class represents each transaction
    """

    transaction_type: str
    transaction_date: datetime.date
    settlement_date: datetime.date  # now eqauls settlement date
    asset_type: str
    symbol: str
    quote: float
    unit: float
    transaction_amount: float
    fee: float = 0.0  # phase 2
    pending: bool = False  # phase 2


@dataclass
class Asset:
    """AssetValue class represents value of each asset at calculation time
    """

    asset_type: str
    cal_date: datetime.date
    latest_quote_date: datetime.date
    symbol: str
    quote: float
    unit: float


class Portfolio:
    """Portfolio class represents a real portfolio
    """

    file_path: Path
    port_name: str
    transactions: List[Transaction] = []
    assets: List[Asset] = []

    def __init__(self, port_name, *, try_to_load=True):
        """constructor

        Arguments:
            port_name {str} -- portfolio name
        """
        self.port_name = port_name

        file_directory = Path.home() / "recport"
        self.file_path = file_directory / f"{port_name}.toml"

        if try_to_load:
            self.loadFromFile()

    def loadFromFile(self):
        """ Load data from file if exists """
        # read portfolio .toml file if exists
        port_name = self.port_name
        file_path = self.file_path
        if file_path.exists():
            # read .toml portfolio config
            logger.debug("Pretend to read file")
            with file_path.open(mode="r") as f:
                doc = parse(f.read())
            transactions = []
            assets = []
            for t in doc["transactions"]:
                transactions.append(
                    Transaction(
                        transaction_type=t["transaction_type"],
                        transaction_date=t["transaction_date"],
                        settlement_date=t["settlement_date"],
                        asset_type=t["asset_type"],
                        symbol=t["symbol"],
                        quote=t["quote"],
                        unit=t["unit"],
                        transaction_amount=t["transaction_amount"],
                        fee=t["fee"],
                        pending=t["pending"],
                    )
                )
            for a in doc["assets"]:
                assets.append(
                    Asset(
                        asset_type=a["asset_type"],
                        cal_date=a["cal_date"],
                        latest_quote_date=a["latest_quote_date"],
                        symbol=a["symbol"],
                        quote=a["quote"],
                        unit=a["unit"],
                    )
                )
            self.transactions = transactions
            self.assets = assets
        else:
            logger.info(
                "🎉 Recport welcome you. 🎉  There is no saved file before. Recport will create a new one."
            )

        # raise NotImplementedError

    def updateToFile(self):
        """ Update/Save data to file, create one if not exists """
        port_name = self.port_name
        transactions = [asdict(t) for t in self.transactions]
        # transactions = [asdict(Transaction('buy', datetime.date(2020,2,8) , datetime.date(2020,2,8), 'cpall', 12.5, 100, 1250, 0, False))]
        assets = [asdict(a) for a in self.assets]
        # assets = [asdict(Asset('stock', datetime.date(2020,2,8), datetime.date(2020,2,8), 12.6, 100))]

        doc = document()
        doc.add("port_name", port_name)
        doc.add("transactions", transactions)
        doc.add("assets", assets)
        file_path = self.file_path
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open(mode="w") as f:

            f.write(doc.as_string())

    def reset(self):
        self.file_path.unlink()
        self.assets = []
        self.transactions = []

    def _fetchClosePrice(self, symbol: str, requested_date: datetime.date) -> dict:
        """internal function to fecth price of stock/mutual fund
        
        Returns:
            float -- stock price / nav

        Raises:
            GetNAVPriceError -- when the price of requested date is not available
            SymbolNotFoundError -- when the symbol is not found
        """
        requested_str_date = str(requested_date)
        try:
            close = float(pdr.get_data_yahoo(symbol)["Close"][requested_str_date])
            asset_type = "stock"

        # symbol not found in stock market, find it in mutual fund
        except pdr._utils.RemoteDataError:
            try:
                a_nav = nav.get(symbol)
                if str(a_nav.updated)[:10] != requested_str_date:
                    raise GetNAVPriceError(
                        f"NAV for symbol {symbol} on {requested_str_date} is not available!"
                    )
                else:
                    close = a_nav.value
                    asset_type = "mutual fund"

            # symbol is not valid
            except KeyError:
                raise SymbolNotFoundError(f"Symbol {symbol} is not found!")

        # symbol is found in stock market, but the price on the date is not available
        except KeyError as x:
            raise GetNAVPriceError(
                f"Price for symbol {symbol} on {requested_str_date} is not available!"
            )

        return {"close": close, "asset_type": asset_type}

    def buy(
        self,
        symbol: str,
        quote: float,
        unit: float,
        transaction_amount: float,
        transaction_date: datetime.date,
    ):

        # recheck if the symbol and price is available for calculation
        data = self._fetchClosePrice(symbol, transaction_date)
        asset_type = data["asset_type"]
        # TODO: Check if there is enough money in the portfolio & if the symbol already exists?
        
        # everthing is fine now, add it in transaction
        transaction = Transaction(
            "buy",
            transaction_date,
            transaction_date,
            asset_type,
            symbol,
            quote,
            unit,
            transaction_amount,
            0.00,
            False,
        )
        self.transactions.append(transaction)

        raise NotImplementedError

    def sell(self, symbol: str, quote: float, unit: float, transaction_amount: float):
        pass

    def interest(self, amount: float):
        pass

    def dividend(self, symbol: str, amount: float):
        pass

    def deposit(self, amount: float):
        pass

    def withdraw(self, amount: float):
        pass

    def __repr__(self):
        return f"Portfolio Obj of '{self.port_name}', contains {len(self.assets)} assets and {len(self.transactions)} transac."


if __name__ == "__main__":
    portfolio = Portfolio("jack")
    logger.debug(portfolio.transactions)
    portfolio.buy("CPALL.BK", 70.50, 100, 7060, datetime.date(2020, 2, 21))
    portfolio.updateToFile()
