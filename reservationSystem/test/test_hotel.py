#!/usr/bin/env python3
"""
test_hotel.py

Unit tests for the Hotel class.
Tests include creating, displaying, modifying, deleting hotels, 
and reserving/canceling room reservations.
"""

import os
import json
import unittest

from app.hotel import Hotel
from app.persistence import HOTEL_FILE

# Helper function to clear the persistence file.
def clear_files():
    """
    Remove the persistence files if they exist.
    """
    if os.path.exists(HOTEL_FILE):
        os.remove(HOTEL_FILE)

class TestHotel(unittest.TestCase):
    """
    Test cases for the Hotel class.
    """

    def setUp(self):
        """
        Clear persistence files before each test.
        """
        clear_files()

    def tearDown(self):
        """
        Clear persistence files after each test.
        """
        clear_files()

    def test_create_and_display_hotel(self):
        """
        Test that a hotel is created and can be displayed.
        """
        hotel = Hotel(1, "Sunrise Inn", "Beach City", 10)
        Hotel.create_hotel(hotel)
        result = Hotel.display_hotel(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Sunrise Inn")

    def test_modify_hotel(self):
        """
        Test modifying hotel attributes.
        """
        hotel = Hotel(2, "Mountain Lodge", "High Peak", 5)
        Hotel.create_hotel(hotel)
        Hotel.modify_hotel(2, {"name": "Mountain Retreat", "total_rooms": 8})
        result = Hotel.display_hotel(2)
        self.assertEqual(result["name"], "Mountain Retreat")
        self.assertEqual(result["total_rooms"], 8)

    def test_delete_hotel(self):
        """
        Test deletion of a hotel.
        """
        hotel = Hotel(3, "City Center Hotel", "Downtown", 20)
        Hotel.create_hotel(hotel)
        Hotel.delete_hotel(3)
        result = Hotel.display_hotel(3)
        self.assertIsNone(result)

    def test_reserve_and_cancel_room(self):
        """
        Test reserving a room and then canceling the reservation.
        """
        hotel = Hotel(4, "Cozy Cottage", "Countryside", 1)
        Hotel.create_hotel(hotel)
        # Reserve a room.
        reserve_success = Hotel.reserve_room(4, 101)
        self.assertTrue(reserve_success)
        hotel_data = Hotel.display_hotel(4)
        self.assertIn(101, hotel_data["reserved_rooms"])

        # Cancel the reservation.
        cancel_success = Hotel.cancel_reservation(4, 101)
        self.assertTrue(cancel_success)
        hotel_data = Hotel.display_hotel(4)
        self.assertNotIn(101, hotel_data["reserved_rooms"])

    def test_reserve_room_fails_when_full(self):
        """
        Test that reserving a room fails when the hotel is full.
        """
        hotel = Hotel(5, "Small Inn", "Quiet Town", 1)
        Hotel.create_hotel(hotel)
        success1 = Hotel.reserve_room(5, 201)
        self.assertTrue(success1)
        # The hotel only has one room; this should fail.
        success2 = Hotel.reserve_room(5, 202)
        self.assertFalse(success2)

if __name__ == "__main__":
    unittest.main()
