from src import backoff_delays
def test_one_shorter_than_attempts(): assert len(backoff_delays(4)) == 3
def test_single_attempt_never_sleeps(): assert backoff_delays(1) == []
def test_exact_sequence(): assert backoff_delays(4) == [1.0, 2.0, 4.0]
