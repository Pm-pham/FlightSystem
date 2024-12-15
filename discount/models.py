import datetime

from django.db import models

# Create your models here.

class Discount:
    def __init__(self, discount_id, name, discount_type, value, start_date, end_date, conditions=None):
        self.discount_id = discount_id
        self.name = name
        self.discount_type = discount_type  # 'percentage' or 'fixed'
        self.value = value
        self.start_date = start_date
        self.end_date = end_date
        self.conditions = conditions  # E.g., {"min_amount": 1000000, "destination": "Hanoi"}

    def is_valid(self):
        current_date = datetime.now()
        return self.start_date <= current_date <= self.end_date

    def calculate_discount(self, total_amount):
        if not self.is_valid():
            return 0
        if self.discount_type == "percentage":
            return total_amount * (self.value / 100)
        elif self.discount_type == "fixed":
            return min(self.value, total_amount)
        return 0
