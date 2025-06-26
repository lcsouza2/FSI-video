def timestamp_to_seconds(ts: str) -> float:
    # Ex: 00:01:09.876 → 1*60 + 9.876 = 69.876
    h, m, s = ts.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)
