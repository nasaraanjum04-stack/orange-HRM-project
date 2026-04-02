
from datetime import datetime, timedelta

def get_future_dates(days_from=1, days_to=2):
    today = datetime.now()
    return (today + timedelta(days=days_from)).strftime("%Y-%d-%m"), (today + timedelta(days=days_to)).strftime("%Y-%d-%m")
