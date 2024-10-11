from datetime import datetime, timedelta

def current_date():
    return datetime.now().strftime('%Y-%m-%d')

def previous_date():
    return (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
