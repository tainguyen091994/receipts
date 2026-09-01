from src import rank
R=[{"n":"a","score":5},{"n":"b","score":9},{"n":"c","score":5},{"n":"d","score":9}]
def test_scores(): assert [r["score"] for r in rank(R)] == [9,9,5,5]
