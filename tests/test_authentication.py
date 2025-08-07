"""
This module contains tests for authentication functioanlity including
login, logout, registration, and password reset.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from configs.test_data import test_data

logger = logging.getLogger(__name__)

class TestAuthentication:
    """Test suite for authentication features"""

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_login(self, page: Page):
        """
        Test successful login with valid credentials.

        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Click login button
        4. Verify redirect to dashboard after login has been successful
        """
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Use test data for valid user
        user = test_data.VALID_USERS[0]
        login_page.login(user['email'], user['password'])

        # Verify successful login
        assert login_page.is_logged_in(), "User should be logged in"


        