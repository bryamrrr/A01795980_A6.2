"""
persistence.py

This module contains functions for loading and saving data from JSON files.
It also defines file path constants for hotels, customers, and reservations.
"""

import json
import os

# Constants for file paths.
HOTEL_FILE = "json/hotels.json"
CUSTOMER_FILE = "json/customers.json"
RESERVATION_FILE = "json/reservations.json"


def load_data(file_path):
    """
    Load data from the given JSON file.

    If the file does not exist or contains invalid JSON, an error is
    printed to the console and an empty list is returned.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: The data loaded from the file.
    """
    if not os.path.exists(file_path):
        return []
    try:
        # Check if the file is empty.
        if os.path.getsize(file_path) == 0:
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading {file_path}: {e}")
        return []


def save_data(file_path, data):
    """
    Save data to the given JSON file.

    Args:
        file_path (str): Path to the JSON file.
        data (list): Data to be saved.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")
