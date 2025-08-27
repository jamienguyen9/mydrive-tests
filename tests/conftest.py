import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0,str(project_root))

import pytest
import logging
from datetime import datetime
from typing import Generator, Dict, Any
from configs.settings import config
from playwright.sync_api import Playwright, Page, Browser, BrowserContext, sync_playwright
from pages.register_page import RegisterPage
from utils.logger import setup_logger
from utils.db_helper import DatabaseHelper
from configs.test_data import test_data

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
    context_options = config.get_browser_context_options()

    # Workaround for fixing permission name issues
    if 'permissions' in context_options:
        valid_permissions = []
        for perm in context_options['permissions']:
            if perm == 'notification':
                valid_permissions.append('notifications')
            elif perm in ['geolocation', 'notifications', 'camera', 'microphone', 'clipboard-read', 'clipboard-write']:
                valid_permissions.append(perm)
        context_options['permissions'] = valid_permissions

    context = browser.new_context(**context_options)

    # Setup request/response logging
    context.on("request", lambda request: logger.debug(f"Request: {request.method} {request.url}"))
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


@pytest.fixture(scope="session")
def db_helper() -> DatabaseHelper:
    """Create a database helper instance"""
    logger.info(f"Connecting to MongoDB with url: {config.mongodb_url}")
    return DatabaseHelper(config.mongodb_url)


@pytest.fixture(scope="module", autouse=True)
def setup_test_users(browser: Browser, db_helper: DatabaseHelper):
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
