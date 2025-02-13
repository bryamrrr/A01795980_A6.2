"""
reservation.py

This module defines the Reservation class which represents a reservation
entity. It provides methods to create and cancel reservations.
Creating a reservation automatically reserves a room at the associated hotel.
"""

from app.persistence import load_data, save_data, RESERVATION_FILE
from app.hotel import Hotel


class Reservation:
    """
    A class representing a reservation.
    """

    def __init__(self, reservation_id, hotel_id, customer_id):
        """
        Initialize a Reservation instance.

        Args:
            reservation_id (int): Unique identifier for the reservation.
            hotel_id (int): ID of the hotel where the reservation is made.
            customer_id (int): ID of the customer who made the reservation.
        """
        self.reservation_id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id

    def to_dict(self):
        """
        Convert the Reservation instance to a dictionary.

        Returns:
            dict: Dictionary representation of the reservation.
        """
        return {
            "reservation_id": self.reservation_id,
            "hotel_id": self.hotel_id,
            "customer_id": self.customer_id
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Reservation instance from a dictionary.

        Args:
            data (dict): Dictionary containing reservation data.

        Returns:
            Reservation: A new Reservation instance.
        """
        return Reservation(
            reservation_id=data.get("reservation_id"),
            hotel_id=data.get("hotel_id"),
            customer_id=data.get("customer_id")
        )

    @staticmethod
    def create_reservation(reservation):
        """
        Create a new reservation linking a customer and a hotel.

        Args:
            reservation (Reservation): The Reservation instance to be added.
        """
        # First, attempt to reserve a room in the hotel.
        if Hotel.reserve_room(
            reservation.hotel_id,
            reservation.reservation_id
        ):
            reservations = load_data(RESERVATION_FILE)
            reservations.append(reservation.to_dict())
            save_data(RESERVATION_FILE, reservations)
        else:
            print("Failed to create reservation due to room unavailability.")

    @staticmethod
    def cancel_reservation(reservation_id):
        """
        Cancel an existing reservation.

        Args:
            reservation_id (int): The reservation ID to cancel.
        """
        reservations = load_data(RESERVATION_FILE)
        reservation_to_cancel = None
        for reservation in reservations:
            if reservation.get("reservation_id") == reservation_id:
                reservation_to_cancel = reservation
                break

        if reservation_to_cancel:
            Hotel.cancel_reservation(
                reservation_to_cancel.get("hotel_id"), reservation_id)
            reservations = [
                r
                for r in reservations
                if r.get("reservation_id") != reservation_id
            ]
            save_data(RESERVATION_FILE, reservations)
        else:
            print("Reservation not found.")
