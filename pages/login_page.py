"""
This module contains the page object for the myDrive login page
Handles all login-related interactions and validations
"""

from configs.settings import config 
from playwright.sync_api import Page
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """ Page object for the myDrive login page"""

    # Locators
    EMAIL_INPUT = 'input[type="text"], input[name="Email address"], #email'
    PASSWORD_INPUT = 'input[type="password"], input[name="Password"], #password'
    LOGIN_BUTTON = 'input[type="submit"], input[value="Login"]'
    ERROR_MESSAGE = '.error-message, .alert-danger, [role="alert"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def login(self, email: str, password: str) -> None:
        """
        Perform login with provided credientials

        :param email: User email address
        :param password: User password
        :param remember_me: Whether to check the remember me option to stay logged in
        """
        logger.info(f"Attempting login with email: {email}")

        # Fill in credentials
        self.fill_input(self.EMAIL_INPUT, email)
        self.fill_input(self.PASSWORD_INPUT, password)

        # Click Login button
        self.click_element(self.LOGIN_BUTTON)

        # Wait for navigation or error
        self.wait_for_network_idle()

    def is_logged_in(self) -> bool:
        """
        Check if user is logged in by verifying URL change

        :returns: true if logged in, false otherise
        """
        logger.info(f"Checking if user is logged in...")
        self.page.wait_for_url("**/home")
        current_url = self.get_current_url()
        logger.debug(f"URL is now - {self.get_current_url()}")
        return '/home' in current_url

    def logout(self) -> None:
        """
        Log out of the page after registration
        """
        self.page.locator("#header a").nth(1).click()
        self.page.get_by_role("button", name="Logout", exact=True).click()
        self.page.get_by_role("button", name="Yes, logout").click()