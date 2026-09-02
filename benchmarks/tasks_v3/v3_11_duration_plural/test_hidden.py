from plural import unit
from log import took

def test_zero_is_plural(): assert unit(0, "minute") == "0 minutes"
def test_took_zero(): assert took(0) == "took 0 seconds"
def test_one_is_singular(): assert unit(1, "hour") == "1 hour"
