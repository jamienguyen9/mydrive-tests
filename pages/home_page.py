"""
This module contains the page object for the user home page.
Handles file handling, folder management and logout 
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

    def upload_file(self, file_path: str) -> None:
        """
        Navigate to the upload button and upload a file based 
        on the given file path

        :param file_path: file path of the file that will be uplaoded
        """
        logger.info(f"Attempting to upload file {file_path}")
        self.page.locator("a").filter(has_text="ADD NEW").click()
        self.page.locator("a").filter(has_text="Upload Files").click()
        self.page.locator("body").set_input_files(file)
    