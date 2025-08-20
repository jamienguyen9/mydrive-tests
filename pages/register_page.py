"""
This module contains the page object for the user registration page. 
Handles user registration and account creation
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
from configs.settings import config
import logging

logger = logging.getLogger(__name__)

class RegisterPage(BasePage):
    """Page object for the registration page"""

    # Locators
    EMAIL_INPUT = 'input[type="text"], input[placeholder="Email address"]'
    CREATE_BUTTON = 'input[type="submit"], input[value="Create"]'

    def __init__(self, page: Page):
        super().__init__(page)

    def register(self, email: str, password: str, unmatching: str = "", click_button: bool = True) -> None:
        """
        Registers a new user account

        :param email: User email
        :param password: User password
        :param unmatching: If not empty, we fill the confirm password input
        box with an unmatching password
        :param click_button: Toggle whether to click the register button
        """
        self.page.get_by_text("Create Account").click()

        logger.info(f"Registering new user: {email}")

        self.fill_input(self.EMAIL_INPUT, email)
        self.page.get_by_role("textbox", name="Password", exact=True).fill(password)
        
        if unmatching:
            self.page.get_by_role("textbox", name="Verify Password").fill(unmatching)
        else:
            self.page.get_by_role("textbox", name="Verify Password").fill(password)

        if click_button:
            self.click_element(self.CREATE_BUTTON)
            self.wait_for_network_idle()

    def logout_after_register(self) -> None:
        """
        Log out of the page after registration
        """
        self.page.locator("#header a").nth(1).click()
        self.page.get_by_role("button", name="Logout", exact=True).click()
        self.page.get_by_role("button", name="Yes, logout").click()
        
        self.wait_for_network_idle()
