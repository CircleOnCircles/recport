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


@dataclass
class Transaction:
    """Transaction class represents each transaction
    """

    transaction_type: str
    transaction_date: datetime.date
    settlement_date: datetime.date  # phase 2
    symbol: str
    quote: float
    unit: float
    transaction_amount: float
    fee: float  # phase 2
    pending: bool  # phase 2


@dataclass
class Asset:
    """AssetValue class represents value of each asset at calculation time
    """

    asset_type: str
    cal_date: datetime.date
    latest_quote_date: datetime.date
    quote: float
    unit: float


class Portfolio:
    """Portfolio class represents a real portfolio
    """

    file_path: Path
    port_name: str
    transactions: List[Transaction] = []
    assets: List[Asset] = []

    def __init__(self, port_name, *, tryToLoad=True):
        """constructor

        Arguments:
            port_name {str} -- portfolio name
        """
        self.port_name = port_name

        file_directory = Path.home() / "recport"
        self.file_path = file_directory / f"{port_name}.toml"

        if tryToLoad:
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

    def buy(self, symbol: str, quote: float, unit: float, transaction_amount: float):
        """ buy stock/mutual fund function updates transaction in memory """
        pass

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


if __name__ == "__main__":
    portfolio = Portfolio("jack")
    logger.debug(portfolio.transactions)
    portfolio.updateToFile()
