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
        logger.info("Deleting users for test teardown...")
        try:
            for user in test_data.VALID_USERS:
                db_helper.delete_test_user(user['email'])
        except Exception as e:
            logger.warning(f"Could not delete user {test_user['email']}: {e}")

    @pytest.mark.smoke
    @pytest.mark.critical
    def test_successful_login(self, page: Page) -> None:
        """
        Test successful login with valid credentials.

        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Click login button
        4. Verify redirect to home page after login has been successful
        """
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Use test data for valid user
        user = test_data.VALID_USERS[0]
        login_page.login(user['email'], user['password'])

        # Verify successful login
        assert login_page.is_logged_in(), "User should be logged in"
        logger.info("Verified login was successful.")

        # Make sure the user is logged out in preparation for the next test
        login_page.logout()

    @pytest.mark.smoke
    def test_login_with_invalid_email(self, page: Page) -> None:
        """
        Test login with an invalid email and verify login was
        unsuccessful

        Steps:
        1. Navigate to login page
        2. Enter invalid credentials
        3. Click login button
        4. Verify we are still in login page with an error message
        """
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Attempt to log in with invalid user
        user = test_data.VALID_USERS[0]
        login_page.login('randomuser.lols@email.com', user['password'])

        # Verify login was not successful
        expect(login_page.page.get_by_text("Incorrect email or password")).to_be_visible()
        assert '/home' not in login_page.get_current_url()
        logger.info("Verified login not successful.")

    @pytest.mark.smoke
    def test_login_with_invalid_password(self, page: Page) -> None:
        """
        Test login with an invalid password and verify login was
        unsuccessful

        Steps:
        1. Navigate to login page
        2. Enter invalid credentials
        3. Click login button
        4. Verify we are still in login page with an error message
        """
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Attempt to log in with invalid user
        user = test_data.VALID_USERS[0]
        login_page.login(user['email'], 'randompasswordhaha')

        # Verify login was not successful
        expect(login_page.page.get_by_text("Incorrect email or password")).to_be_visible()
        assert '/home' not in login_page.get_current_url()
        logger.info("Verified login not successful.")

        
    @pytest.mark.smoke
    def test_login_with_invalid_credentials(self, page: Page) -> None:
        """
        Test login with an invalid credentials and verify login was
        unsuccessful

        Steps:
        1. Navigate to login page
        2. Enter invalid credentials
        3. Click login button
        4. Verify we are still in login page with an error message
        """
        login_page = LoginPage(page)
        login_page.navigate_to()

        # Attempt to log in with invalid user
        login_page.login('randomuser.lols@email.com', 'java smells')

        # Verify login was not successful
        expect(login_page.page.get_by_text("Incorrect email or password")).to_be_visible()
        assert '/home' not in login_page.get_current_url()
        logger.info("Verified login was not successful.")

    @pytest.mark.smoke
    def test_registration_and_logout(self, page: Page) -> None:
        """
        Test user registration flow

        Steps:
        1. Navigate to login page
        2. Register an account using valid credentials
        3. Verify page navigates to user home page after registration
        4. Logout of user account
        5. Verify we are back to user login page
        """
        register_page = RegisterPage(page)
        register_page.navigate_to()

        test_user = test_data.VALID_USERS[1]
        register_page.register(test_user["email"], test_user["password"])
        
        expect(register_page.page.get_by_role("heading", name="Quick Access")).to_be_visible()
        logger.info("Verified user has logged in after successful registration")

        register_page.logout_after_register()
        expect(register_page.page.get_by_text("Login to your account")).to_be_visible()
        logger.info("Verified logout was successful")

    @pytest.mark.smoke
    def test_register_with_non_email(self, page: Page) -> None:
        """
        Test user registration with non-email

        Steps:
        1. Navigate to login page
        2. Attempt to register an account using a non-email
        3. Verify an error occurs saying that the email is invalid
        """
        register_page = RegisterPage(page)
        register_page.navigate_to()

        test_user = {
            "email": "jimmyscroissants",
            "password": "croissants"
        }
        register_page.register(test_user["email"], test_user["password"], click_button=False)

        expect(register_page.page.get_by_text("Email is invalid")).to_be_visible()
        logger.info("Verified user registration was not successful due to invalid email")

    @pytest.mark.smoke
    def test_register_with_short_password(self, page: Page) -> None:
        """
        Test user registration with short passwords

        Steps:
        1. Navigate to login page
        2. Attempt to register an account with a really short password
        3. Verify an error occurs saying that the password must be at least 6 characters
        """
        register_page = RegisterPage(page)
        register_page.navigate_to()

        test_user = {
            "email": "carlwheezer@email.com",
            "password": "hah"
        }
        register_page.register(test_user["email"], test_user["password"], click_button=False)

        expect(register_page.page.get_by_text("Password must be at least 6")).to_be_visible()
        logger.info("Verified user registration was not successful due to short password")



    @pytest.mark.smoke
    def test_register_with_unmatching_passwords(self, page: Page) -> None:
        """
        Test user registration with unmatching passwords

        Steps:
        1. Navigate to login page
        2. Attempt to register an account with a really short password
        3. Verify an error occurs saying that the passwords do not match
        """
        register_page = RegisterPage(page)
        register_page.navigate_to()

        test_user = {
            "email": "carlwheezer@email.com",
            "password": "jimmysmom"
        }
        register_page.register(test_user["email"], test_user["password"], "hahaha", click_button=False)

        expect(register_page.page.get_by_text("Passwords do not match")).to_be_visible()
        logger.info("Verified user registration was not successful due to unmatching passwords")
