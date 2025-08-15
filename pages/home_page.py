"""
This module contains the page object for the user home page.
Handles image upload and logout stuff idk yet
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Page object for the user home page"""

    def __init__(self, page: Page):
        super().__init__(page)

    def logout(self) -> None:
        """Log out of the page"""
        logger.info("Logging out of the home page")
        self.page.locator("#header a").nth(1).click()
        self.page.get_by_role("button", name="Logout", exact=True).click()
        self.page.get_by_role("button", name="Yes, logout").click()
        logger.info("Logged out")
