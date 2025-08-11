"""
This module contains the base page class that all other page objects inherit from.
Provides common functionality for page interactions, element waiting, and error handling.
"""

import logging
from typing import Optional, List, Dict, Any, Union
from playwright.sync_api import Page, Locator, expect, TimeoutError as PlaywrightTimeoutError
from configs.settings import config
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class BasePage:
    """
    Base class for all page objects
    Provides common methods for page interactions and element handling
    """

    def __init__(self, page: Page):
        self.page = page
        self.timeout = config.default_timeout

    def navigate_to(self, url: Optional[str] = None) -> None:
        """
        Navigate to a specific URL or the base URL

        :param url: Optional URL to navigate to. Uses base_url if not provided 
        """
        target_url = url or config.base_url
        logger.info(f"Navigating to: {target_url}")
        self.page.goto(target_url, **config.get_page_goto_options())

    def wait_for_element(self, selector: str, state: str = 'visible',
                        timeout: Optional[int] = None) -> Locator:
        """
        Wait for an element to reach a specific state

        :param selector: Element selector
        :param state: State to wait for (visible, hidden, attached, detached)
        :param timeout: Custom timeout in ms
        :returns: Locator for the element
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for element: {selector} to be {state}")

        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator

    def click_element(self, selector: str, force: bool = False,
                        timeout: Optional[int] = None) -> None:
        """
        Click on an element with error handling

        :param selector: Element selector
        :param force: Force click even if element is not visible
        :param timeout: Custom timeout in ms
        """
        try:
            element = self.wait_for_element(selector, timeout=timeout)
            logger.debug(f"Clicking element: {selector}")
            element.click(force=force)
        except PlaywrightTimeoutError:
            logger.error(f"Failed to click element: {selector}")
            # TODO: Create screenshot method in this class
            raise
    
    def fill_input(self, selector: str, text: str,
                    clear_first: bool = True) -> None:
        """
        Fill an input field with text

        :param selector: Input field selector
        :param text: Text to enter in the input field
        :clear_first: Whether to clear the field before entering first
        """
        element = self.wait_for_element(selector)
        logger.debug(f"Filling input '{selector}' with text: {text[:20]}...")

        if clear_first:
            element.clear()
        element.fill(text)
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content from an element

        :param selector: Element selector
        :param timeout: Custom timeout in ms
        :returns: Text content of the element
        """
        element = self.wait_for_element(selector, timeout=timeout)
        return element.text_content() or ""

    def is_element_visible(self, selector: str, timeout: int = 1000) -> bool:
        """
        Check if an element is visible

        :param selector: Element selector
        :param timeout: Timeout for checking visibility
        :returns: True if element is visible, false otherwise
        """
        try:
            self.wait_for_element(selector, state='visible', timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_network_idle(self, timeout: Optional[int] = None) -> None:
        """Wait for network to be idle"""
        timeout = timeout or self.timeout
        self.page.wait_for_load_state('networkidle', timeout=timeout)
