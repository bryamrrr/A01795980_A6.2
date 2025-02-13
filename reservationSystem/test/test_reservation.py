#!/usr/bin/env python3
"""
test_reservation.py

Unit tests for the Reservation class.
Tests include creating and canceling reservations.
"""

import os
import json
import unittest

from app.reservation import Reservation
from app.hotel import Hotel
from app.customer import Customer
from app.persistence import RESERVATION_FILE

# Helper function to clear the reservation persistence file.
def clear_files():
    """
    Remove the reservation persistence file if it exists.
    """
    if os.path.exists(RESERVATION_FILE):
        os.remove(RESERVATION_FILE)

class TestReservation(unittest.TestCase):
    """
    Test cases for the Reservation class.
    """

    def setUp(self):
        """
        Clear persistence files and create a hotel and customer for reservations.
        """
        clear_files()
        # Ensure a hotel and customer exist for the reservation.
        hotel = Hotel(10, "Lakeside Resort", "Lakeview", 2)
        Hotel.create_hotel(hotel)
        customer = Customer(10, "Dana White", "dana@example.com", "555-1111")
        Customer.create_customer(customer)

    def tearDown(self):
        """
        Clear persistence files after each test.
        """
        clear_files()

    def test_create_reservation(self):
        """
        Test that a reservation is created and stored.
        """
        reservation = Reservation(301, 10, 10)
        Reservation.create_reservation(reservation)
        # Load reservations from file.
        with open(RESERVATION_FILE, "r", encoding="utf-8") as f:
            reservations = json.load(f)
        res_ids = [r["reservation_id"] for r in reservations]
        self.assertIn(301, res_ids)

    def test_cancel_reservation(self):
        """
        Test canceling an existing reservation.
        """
        reservation = Reservation(302, 10, 10)
        Reservation.create_reservation(reservation)
        # Verify the reservation was created.
        with open(RESERVATION_FILE, "r", encoding="utf-8") as f:
            reservations = json.load(f)
        res_ids = [r["reservation_id"] for r in reservations]
        self.assertIn(302, res_ids)
        # Cancel the reservation.
        Reservation.cancel_reservation(302)
        with open(RESERVATION_FILE, "r", encoding="utf-8") as f:
            reservations = json.load(f)
        res_ids = [r["reservation_id"] for r in reservations]
        self.assertNotIn(302, res_ids)

    def test_cancel_nonexistent_reservation(self):
        """
        Test canceling a reservation that does not exist.
        """
        from io import StringIO
        import sys

        # Capture printed output.
        captured_output = StringIO()
        sys.stdout = captured_output
        Reservation.cancel_reservation(999)
        sys.stdout = sys.__stdout__
        self.assertIn("Reservation not found", captured_output.getvalue())

if __name__ == "__main__":
    unittest.main()
