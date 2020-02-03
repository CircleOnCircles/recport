from pathlib import Path
from loguru import logger
from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import table

class Portfolio:
    """Portfolio class represents a real portfolio
    """

    def __init__(self, port_name):
        """constructor
        
        Arguments:
            port_name {str} -- portfolio name
        """
        self.port_name = port_name

        file_directory = Path.home() / "recport"
        self.file_path = file_directory / f"{port_name}.toml"

        self.loadFromFile()

    def loadFromFile(self):
        """ Load data from file if exists """
        # read portfolio .toml file if exists
        if file_path.exists():
            # read .toml portfolio config
            logger.debug('Pretend to read file')

        raise NotImplementedError

    def updateTofile(self):
        """ Update/Save data to file, create one if not exists """
        port_name = self.port_name
        file_path = self.file_path

        doc = document()
        doc.add('port_name',port_name)
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with file_path.open(mode='w') as f:
            
            f.write(doc.as_string())


    def buy(self, symbol: str, quote: float, unit: float, transaction_amount: float):
        pass

    def sell(self):
        pass

    def r_int(self):
        pass

    def deposit(self):
        pass

    def withdraw():
        pass

if __name__ == "__main__":
    portfolio = Portfolio('jack')



