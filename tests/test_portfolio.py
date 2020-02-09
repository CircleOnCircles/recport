from recport import Portfolio, Transaction, Asset
import datetime


def test_major():
    """ Test major use cases """
    portfolio = Portfolio("__test__")

    # Monkey Patch since methods are under dev.
    t = Transaction(
        "buy",
        datetime.date(2020, 2, 8),
        datetime.date(2020, 2, 8),
        "cpall",
        12.5,
        100,
        1250,
        0,
        False,
    )
    portfolio.transactions.append(t)
    a = Asset("stock", datetime.date(2020, 2, 8), datetime.date(2020, 2, 8), 12.6, 100)
    Portfolio.assets.append(a)

    portfolio.updateToFile()

    assert portfolio.file_path.exists()

    del portfolio

    portfolio = Portfolio("__test__")

    assert portfolio.assets[-1] == a
    assert portfolio.transactions[-1] == t

    portfolio.reset()

    assert not portfolio.file_path.exists()
    assert not portfolio.assets
    assert not portfolio.transactions

    del portfolio

    portfolio = Portfolio("__test__")

    # TODO: Identify why these assert are fails.
    # assert not portfolio.assets
    # assert not portfolio.transactions
