import json
import os

def load_data(file_path):
    """
    Load JSON data from a file.
    
    :param file_path: Path to the JSON file.
    :return: Data loaded from the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from the file {file_path}: {e}")

    return data

def process_data(data):
    """
    Process the loaded data.
    
    :param data: Data to process.
    :return: Processed data.
    """
    # Example processing: Normalize numerical data
    if not isinstance(data, list):
        raise ValueError("Data should be a list of dictionaries.")

    processed_data = []
    for item in data:
        if isinstance(item, dict):
            processed_item = {k: (v / 100.0 if isinstance(v, (int, float)) else v) for k, v in item.items()}
            processed_data.append(processed_item)
        else:
            raise ValueError("Each item in the data list should be a dictionary.")

    return processed_data

def save_processed_data(data, output_file):
    """
    Save processed data to a JSON file.
    
    :param data: Processed data to save.
    :param output_file: Path to the output file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
if __name__ == "__main__":
    input_file = 'data/sample_data.json'
    output_file = 'data/processed_data.json'
    
    # Load data
    try:
        data = load_data(input_file)
        print(f"Loaded data: {data}")
    except (FileNotFoundError, ValueError) as e:
        print(e)
    
    # Process data
    try:
        processed_data = process_data(data)
        print(f"Processed data: {processed_data}")
    except ValueError as e:
        print(e)
    
    # Save processed data
    save_processed_data(processed_data, output_file)
    print(f"Processed data saved to {output_file}")
