def filter_data(data, filter_key, filter_value):
    if isinstance(data, list):
        return [item for item in data if str(item.get(filter_key, '')).lower() == str(filter_value).lower()]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if str(v.get(filter_key, '')).lower() == str(filter_value).lower()}
    else:
        return data
