from src.filter_data import filter_data

def print_value(data, value_key, filter_key, filter_value):
    filtered_data = filter_data(data, filter_key, filter_value)
    if filtered_data:
        if isinstance(filtered_data, list):
            for item in filtered_data:
                print(f"{value_key}: {item.get(value_key, 'Not found')}")
        elif isinstance(filtered_data, dict):
            print(f"{value_key}: {filtered_data.get(value_key, 'Not found')}")
    else:
        print(f"No data found matching the filter: {filter_key}={filter_value}")
