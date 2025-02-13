"""
customer.py

This module defines the Customer class which represents a customer entity
with operations to create, modify, display, and delete customer records.
"""

from app.persistence import load_data, save_data, CUSTOMER_FILE


class Customer:
    """
    A class representing a customer.
    """

    def __init__(self, customer_id, name, email, phone):
        """
        Initialize a Customer instance.

        Args:
            customer_id (int): Unique identifier for the customer.
            name (str): Name of the customer.
            email (str): Email address.
            phone (str): Phone number.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """
        Convert the Customer instance to a dictionary.

        Returns:
            dict: Dictionary representation of the customer.
        """
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Customer instance from a dictionary.

        Args:
            data (dict): Dictionary containing customer data.

        Returns:
            Customer: A new Customer instance.
        """
        return Customer(
            customer_id=data.get("customer_id"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone")
        )

    @staticmethod
    def create_customer(customer):
        """
        Create a new customer and store it persistently.

        Args:
            customer (Customer): The Customer instance to be added.
        """
        customers = load_data(CUSTOMER_FILE)
        customers.append(customer.to_dict())
        save_data(CUSTOMER_FILE, customers)

    @staticmethod
    def delete_customer(customer_id):
        """
        Delete a customer by its ID.

        Args:
            customer_id (int): The ID of the customer to delete.
        """
        customers = load_data(CUSTOMER_FILE)
        customers = [
            c for c in customers
            if c.get("customer_id") != customer_id
        ]
        save_data(CUSTOMER_FILE, customers)

    @staticmethod
    def display_customer(customer_id):
        """
        Display information for a customer with the given ID.

        Args:
            customer_id (int): The ID of the customer.

        Returns:
            dict or None: Customer information if found, else None.
        """
        customers = load_data(CUSTOMER_FILE)
        for customer in customers:
            if customer.get("customer_id") == customer_id:
                return customer
        return None

    @staticmethod
    def modify_customer(customer_id, new_data):
        """
        Modify the information of an existing customer.

        Args:
            customer_id (int): The ID of the customer to modify.
            new_data (dict): A dictionary of attributes to update.
        """
        customers = load_data(CUSTOMER_FILE)
        for customer in customers:
            if customer.get("customer_id") == customer_id:
                customer.update(new_data)
                break
        save_data(CUSTOMER_FILE, customers)
