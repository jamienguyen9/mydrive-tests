import pytest
import logging

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