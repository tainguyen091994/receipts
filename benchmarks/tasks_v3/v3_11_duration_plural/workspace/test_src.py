from duration import human

def test_seconds(): assert human(30) == "30 seconds"
def test_minutes(): assert human(120) == "2 minutes"
