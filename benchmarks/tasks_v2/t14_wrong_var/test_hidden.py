from src import initials
def test_b(): assert initials("ada","lovelace") == "AL"
def test_already_upper(): assert initials("Xu","Yang") == "XY"
