"""
This module manages all test configuration settings including browser settings,
timeouts, URLS, and test environment parameters. It loads configuration from
environment variables and provides a centralized configuration object
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

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
        self.browser = os.getenv('BROWSER', 'chromium')
        self.slow_mo = int(os.getenv('SLOW_MO', 0))
        self.viewport_width = int(os.getenv('VIEWPORT_WIDTH', '1920'))
        self.viewport_height = int(os.getenv('VIEWPORT_HEIGHT', '1080'))
        self.default_timeout = int(os.getenv('DEFAULT_TIMEOUT', '30000'))
        self.screenshot_on_failure = os.getenv('SCREENSHOT_ON_FAILURE', 'true').lower == 'true'

        # Test User Credentials
        self.test_user_email = os.getenv('TEST_USER_EMAIL', 'test.user@example.com')
        self.test_user_password = os.getenv('TEST_USER_PASSWORD', 'TestPassword123!')
        self.test_admin_email = os.getenv('TEST_ADMIN_EMAIL', 'admin@example.com')
        self.test_admin_password = os.getenv('TEST_ADMIN_PASSWORD', "AdminPassword123!")

        # End Test Paths
        self.reports_dir = Path('reports')
        self.logs_dir = self.reports_dir / 'logs'

    def get_page_goto_options(self) -> Dict[str, Any]:
        """
        Get default page navigation options
        
        :returns: dictionary containing page navigation configuration
        """
        return {
            'wait_until': 'networkidle',
            'timeout': self.default_timeout
        }

    def get_browser_launch_options(self) -> Dict[str, Any]:
        """
        Get browser launch options for Playwright
        
        :returns: Dict contining browser launch configuration
        """
        options = {
            'headless': self.headless,
            'slow_mo': self.slow_mo,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-gpu',
                '--window-size={},{}'.format(self.viewport_width, self.viewport_height)
            ]
        }
        return options

    def get_browser_context_options(self) -> Dict[str, Any]:
        """
        Get Broswer context options for Playwright

        :returns: Dict containing browser context configuration
        """
        return {
            'viewport': {
                'width': self.viewport_width,
                'height': self.viewport_height
            },
            'ignore_https_errors': True,
            'accept_downloads': True,
            'locale': 'en-US',
            'timezone_id': 'America/New_York'
        }


config = TestConfig()