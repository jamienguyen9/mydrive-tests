"""
This module manages all test configuration settings including browser settings,
timeouts, URLS, and test environment parameters. It loads configuration from
environment variables and provides a centralized configuration object
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

load_dotenv('.env.test')

class TestConfig:
    """
    Central configuration class for test settings
    Manages all configuration paramters needed for test execution
    """

    def __init__(self):
        """Initialize configuration by loading environment variables"""

        # Test Environment Browser configuration
        self.base_url = os.getenv('BASE_URL', 'http://localhost:3000')
        self.headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        self.default_timeout = int(os.getenv('DEFAULT_TIMEOUT', '30000'))
        self.screenshot_on_failure = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower == 'true'

        # Test User Credentials
        self.test_user_email = os.getenv('TEST_USER_EMAIL', 'test.user@example.com')
        self.test_user_password = os.getenv('TEST_USER_PASSWORD', 'TestPassword123!')
        self.test_admin_email = os.getenv('TEST_ADMIN_EMAIL', 'admin@example.com')
        self.test_admin_password = os.getenv('TEST_ADMIN_PASSWORD', "AdminPassword123!")

    def get_page_goto_options(self) -> Dict[str, Any]:
        """
        Get default page navigation options
        
        :returns: dictionary containing page navigation configuration
        """
        return {
            'wait_until': 'networkidle',
            'timeout': self.default_timeout
        }