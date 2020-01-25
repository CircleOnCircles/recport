from pathlib import Path

from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import table



home = Path.home()



class Portfolio:

    def __init__(self, port_name):
        """constructor
        
        Arguments:
            port_name {str} -- portfolio name
        """
        self.port_name = port_name
        doc = document()
        doc.add('port_name',self.port_name)
        with open(Path.joinpath(home,Path('test.toml')), 'w') as f:
            f.write(doc.as_string())

if __name__ == "__main__":
    portfolio = Portfolio('jack')



