from src import backoff_delays
def test_cap_applied(): assert max(backoff_delays(10)) == 30.0
def test_base_respected(): assert backoff_delays(3, base=2.0)[0] == 2.0
