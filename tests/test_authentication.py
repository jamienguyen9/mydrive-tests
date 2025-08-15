"""
This module contains tests for authentication functioanlity including
login, logout, registration, and password reset.
"""

import pytest
import logging
from playwright.sync_api import Page, expect, Browser
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.db_helper import DatabaseHelper
from configs.test_data import test_data

logger = logging.getLogger(__name__)

class TestAuthentication:
    """Test suite for authentication features"""

    @pytest.fixture(scope="class", autouse=True)
    def setup_test_users(self, browser: Browser, db_helper: DatabaseHelper):
        context = browser.new_context()
        page = context.new_page()

        register_page = RegisterPage(page)
        register_page.navigate_to()
        
        test_user = test_data.VALID_USERS[0]
        register_page.register(test_user['email'], test_user['password'])
        register_page.logout_after_register()

        logger.info("Register successful")
        context.close()

        yield

        # Delete test users after test
        try:
            db_helper.delete_test_user(test_user['email'])
        except Exception as e:
            logger.warning(f"Could not delete user {test_user['email']}: {e}")

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
        logger.info("Login successful.")
