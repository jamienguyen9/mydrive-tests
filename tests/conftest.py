import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0,str(project_root))

import pytest
import logging
from typing import Generator, Dict, Any
from configs.settings import config
from playwright.sync_api import Playwright, Page, Browser, BrowserContext, sync_playwright
from utils.logger import setup_logger

logger = setup_logger(__name__)

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """
    Create a Playwright instance for the test sesh
    """
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Create a browser instance for the test session
    """
    browser_type = getattr(playwright_instance, config.browser)
    browser = browser_type.launch(**config.get_browser_launch_options())

    yield browser
    
    browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Create a browser context for each test function
    """
    context = browser.new_context(**config.get_browser_context_options())

    # Setup request/response logging
    context.on("request", lambda request: logger.debug(f"Request: {request.method} {request.utl}"))
    context.on("response", lambda response: logger.debug(f"Response: {response.status} {response.url}"))

    # context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # context.tracing.stop()
    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Create a page for each test function
    """
    page = context.new_page()
    page.set_default_timeout(config.default_timeout)
    page.goto(config.base_url)

    yield page

    # TODO Take screenshot of page on failure

    page.close()
    

@pytest.fixture(scope="function", autouse=True)
def test_setup_teardown(request):
    """Setup and teardown for each test"""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")

    yield

    # Mark test failure for screenshot capture
    if request.node.rep_call.failed:
        pytest._test_failed = True
    else:
        pytest._test_failed = False

    logger.info(f"Finished test: {test_name}")