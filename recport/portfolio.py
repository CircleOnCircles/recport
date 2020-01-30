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

        file_directory = Path(Path.home() / "recport")
        file_path = Path(file_directory / f"{port_name}.toml")

        # read portfolio .toml file if exists
        if file_path.exists():
            # read .toml portfolio config
            logger.debug('Pretend to read file')

        # if not, create new portfolio .toml file
        else:
            doc = document()
            doc.add('port_name',port_name)
            if not file_directory.exists():
                file_directory.mkdir(parents=True)
            with Path(file_path).open(mode='w') as f:
                
                f.write(doc.as_string())

        self.port_name = port_name

if __name__ == "__main__":
    portfolio = Portfolio('jack')



