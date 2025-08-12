"""
Module that provides utilities for database operations during testing.
Includes creating test users, cleaning up test data, and verifying data. 
"""

from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any, Optional, List
import hashlib
import logging

logger = logging.getLogger(__name__)

class DatabaseHelper:
    """ Helper class for database operations during testing"""

    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string)
        logger.info(f"Listing database names: {self.client.list_database_names()}")
        self.db = self.client.get_database()

    def create_test_user(self, user_data: Dict[str, Any]) -> str:
        """ 
        Create a test user in the database
        
        :param user_data: Dict containing user info
        :returns: User ID of the created test user
        """
        password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()

        user_doc = {
            'email': user_data['email'],
            'password': password_hash,
            'firstName': user_data.get('first_name', ''),
            'lastName': user_data.get('last_name', ''),
            'createdAt': datetime.utcnow(),
            'isTestUser': True,
            'emailVerified': True,
            'storageUsed': 0,
            'storageLimit': 1024 * 1024 * 1024  # 1GB limit
        }

        result = self.db.users.insert_one(user_doc)
        logger.info(f"Created test user: {user_data['email']}")
        return str(result.inserted_id)

    def delete_test_user(self, email: str) -> bool:
        """
        Delete a test user and associated data

        :params email: User email
        :returns: True if the user was deleted
        """
        if not user:
            return False
        
        user_id = user['_id']
        self.db.files.delete_many({'userId': user_id})
        self.db.folders.delete_many({'userId': user_id})
        result = self.db.users.delete_one({'userId': user_id})
        
        logger.info(f"Deleted test user: {email}")
        return result.deleted_count > 0

    def cleanup_test_data(self) -> None:
        """Cleans up all test data from database"""
        test_users = self.db.users.find({'isTestUser': True})
        for user in test_users:
            self.delete_test_user(user['email'])

        logger.info("Cleaned up all tet data")