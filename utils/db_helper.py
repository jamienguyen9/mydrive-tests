"""
Module that provides utilities for database operations during testing.
Includes creating test users, cleaning up test data, and verifying data. 
"""

from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse
import hashlib
import bcrypt
import logging

logger = logging.getLogger(__name__)

class DatabaseHelper:
    """ Helper class for database operations during testing"""

    def __init__(self, connection_string: str, db_name: Optional[str] = None):
        self.connection_string = connection_string
        self.client = None
        self.db = None
        
        try:
            # Create MongoDB client
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            
            if db_name:
                self.db = self.client[db_name]
            else:
                parsed_url = urlparse(connection_string)
                
                if parsed_url.path and len(parsed_url.path) > 1:
                    db_name_from_url = parsed_url.path[1:].split('?')[0]
                    if db_name_from_url:
                        self.db = self.client[db_name_from_url]
                    else:
                        # Default database name
                        self.db = self.client['mydrive_test']
                else:
                    # Default database name
                    self.db = self.client['mydrive_test']
            
            # Test the connection
            self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB database: {self.db.name}")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except ConfigurationError as e:
            logger.error(f"MongoDB configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise

    def delete_test_user(self, email: str) -> bool:
        """
        Delete a test user and associated data

        :params email: User email
        :returns: True if the user was deleted
        """
        try:
            user = self.db.users.find_one({'email': email})
            if not user:
                logger.warning(f"User not found for deletion: {email}")
                return False
            
            user_id = user['_id']
            
            # Delete user's files and folders
            files_result = self.db.files.delete_many({'userId': user_id})
            logger.debug(f"Deleted {files_result.deleted_count} files for user {email}")

            folders_result = self.db.folders.delete_many({'userId': user_id})
            logger.debug(f"Deleted {folders_result.deleted_count} folders for user {email}")
            
            result = self.db.users.delete_one({'_id': user_id})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted test user: {email}")
                return True
            else:
                logger.warning(f"Failed to delete user: {email}")
                return False
        except Exception as e:
            logger.error(f"Error when deleting test user {email}: {e}")
            return False

    def cleanup_test_data(self) -> None:
        """Cleans up all test data from database"""
        test_users = self.db.users.find({'isTestUser': True})
        for user in test_users:
            self.delete_test_user(user['email'])

        logger.info("Cleaned up all tet data")