def collect(item, bucket=None):
    bucket = bucket or []
    bucket.append(item)
    return bucket
