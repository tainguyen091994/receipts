from src import split_evenly
# the docstring says EARLIER parts absorb the remainder. A fix that appends the
# remainder to the last part sums correctly and still fails these.
def test_remainder(): assert split_evenly(10, 3) == [4,3,3]
def test_remainder_2(): assert split_evenly(11, 4) == [3,3,3,2]
def test_more_parts_than_total(): assert split_evenly(2, 5) == [1,1,0,0,0]
