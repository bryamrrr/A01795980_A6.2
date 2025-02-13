"""
hotel.py

This module defines the Hotel class which represents a hotel entity
with operations to create, modify, display, and delete hotel records,
as well as to reserve and cancel room reservations.
"""

from app.persistence import load_data, save_data, HOTEL_FILE


class Hotel:
    """
    A class representing a hotel.
    """

    def __init__(self,
                 hotel_id,
                 name,
                 location,
                 total_rooms,
                 reserved_rooms=None):
        """
        Initialize a Hotel instance.

        Args:
            hotel_id (int): Unique identifier for the hotel.
            name (str): Name of the hotel.
            location (str): Location of the hotel.
            total_rooms (int): Total number of rooms.
            reserved_rooms (list, optional): List of reservation IDs.
                Defaults to an empty list.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.reserved_rooms = (
            reserved_rooms
            if reserved_rooms is not None
            else []
        )

    def to_dict(self):
        """
        Convert the Hotel instance to a dictionary.

        Returns:
            dict: Dictionary representation of the hotel.
        """
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "reserved_rooms": self.reserved_rooms
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Hotel instance from a dictionary.

        Args:
            data (dict): Dictionary containing hotel data.

        Returns:
            Hotel: A new Hotel instance.
        """
        return Hotel(
            hotel_id=data.get("hotel_id"),
            name=data.get("name"),
            location=data.get("location"),
            total_rooms=data.get("total_rooms"),
            reserved_rooms=data.get("reserved_rooms", [])
        )

    @staticmethod
    def create_hotel(hotel):
        """
        Create a new hotel and store it persistently.

        Args:
            hotel (Hotel): The Hotel instance to be added.
        """
        hotels = load_data(HOTEL_FILE)
        hotels.append(hotel.to_dict())
        save_data(HOTEL_FILE, hotels)

    @staticmethod
    def delete_hotel(hotel_id):
        """
        Delete a hotel by its ID.

        Args:
            hotel_id (int): The ID of the hotel to delete.
        """
        hotels = load_data(HOTEL_FILE)
        hotels = [h for h in hotels if h.get("hotel_id") != hotel_id]
        save_data(HOTEL_FILE, hotels)

    @staticmethod
    def display_hotel(hotel_id):
        """
        Display information for a hotel with the given ID.

        Args:
            hotel_id (int): The ID of the hotel.

        Returns:
            dict or None: Hotel information if found, else None.
        """
        hotels = load_data(HOTEL_FILE)
        for hotel in hotels:
            if hotel.get("hotel_id") == hotel_id:
                return hotel
        return None

    @staticmethod
    def modify_hotel(hotel_id, new_data):
        """
        Modify the information of an existing hotel.

        Args:
            hotel_id (int): The ID of the hotel to modify.
            new_data (dict): A dictionary of attributes to update.
        """
        hotels = load_data(HOTEL_FILE)
        for hotel in hotels:
            if hotel.get("hotel_id") == hotel_id:
                hotel.update(new_data)
                break
        save_data(HOTEL_FILE, hotels)

    @staticmethod
    def reserve_room(hotel_id, reservation_id):
        """
        Reserve a room at a given hotel by adding a reservation ID.

        Args:
            hotel_id (int): The ID of the hotel.
            reservation_id (int): The reservation ID to add.

        Returns:
            bool: True if successful, False otherwise.
        """
        hotels = load_data(HOTEL_FILE)
        updated = False
        for hotel in hotels:
            if hotel.get("hotel_id") == hotel_id:
                if (
                    len(hotel.get("reserved_rooms", []))
                    < hotel.get("total_rooms", 0)
                ):
                    hotel["reserved_rooms"].append(reservation_id)
                    updated = True
                else:
                    print("No available rooms in this hotel.")
                break
        save_data(HOTEL_FILE, hotels)
        return updated

    @staticmethod
    def cancel_reservation(hotel_id, reservation_id):
        """
        Cancel a reservation at a given hotel by removing the reservation ID.

        Args:
            hotel_id (int): The ID of the hotel.
            reservation_id (int): The reservation ID to remove.

        Returns:
            bool: True if successful, False otherwise.
        """
        hotels = load_data(HOTEL_FILE)
        updated = False
        for hotel in hotels:
            if hotel.get("hotel_id") == hotel_id:
                if reservation_id in hotel.get("reserved_rooms", []):
                    hotel["reserved_rooms"].remove(reservation_id)
                    updated = True
                break
        save_data(HOTEL_FILE, hotels)
        return updated
