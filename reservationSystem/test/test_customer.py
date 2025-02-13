#!/usr/bin/env python3
"""
test_customer.py

Unit tests for the Customer class.
Tests include creating, displaying, modifying, and deleting customers.
"""

import os
import unittest

from app.customer import Customer
from app.persistence import CUSTOMER_FILE

# Helper function to clear the persistence file.
def clear_files():
    """
    Remove the customer persistence file if it exists.
    """
    if os.path.exists(CUSTOMER_FILE):
        os.remove(CUSTOMER_FILE)

class TestCustomer(unittest.TestCase):
    """
    Test cases for the Customer class.
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

    def test_create_and_display_customer(self):
        """
        Test that a customer is created and can be displayed.
        """
        customer = Customer(1, "Alice Smith", "alice@example.com", "555-1234")
        Customer.create_customer(customer)
        result = Customer.display_customer(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Alice Smith")

    def test_modify_customer(self):
        """
        Test modifying a customer's attributes.
        """
        customer = Customer(2, "Bob Jones", "bob@example.com", "555-5678")
        Customer.create_customer(customer)
        Customer.modify_customer(2, {"email": "bobjones@example.com"})
        result = Customer.display_customer(2)
        self.assertEqual(result["email"], "bobjones@example.com")

    def test_delete_customer(self):
        """
        Test deletion of a customer.
        """
        customer = Customer(3, "Charlie Brown", "charlie@example.com", "555-0000")
        Customer.create_customer(customer)
        Customer.delete_customer(3)
        result = Customer.display_customer(3)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()
