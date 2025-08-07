"""
This module contains all test data constants used throughout the test suite
Provides sample data for test scenarios including user data, file info, and
test content
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import random
import string

class TestData:
    """Container class for all test data constants"""

    # Valid user test data
    VALID_USERS = [
        {
            'email': 'john.doe@example.com',
            'password': 'JohnDoe123!',
            'first_name': 'John',
            'last_name': 'Doe'
        },
        {
            'email': 'jane.smith@example.com',
            'password': 'JaneSmith456!',
            'first_name': 'Jane',
            'last_name': 'Smith'
        },
        {
            'email': 'test.automation@example.com',
            'password': 'TestAuto789!',
            'first_name': 'Test',
            'last_name': 'Auto'
        },
    ]

test_data = TestData()