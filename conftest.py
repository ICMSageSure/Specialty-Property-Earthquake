import pytest
from playwright.sync_api import Page

from actions import LoginActions, QuoteActions
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width": 1920, "height": 1080}}


@pytest.fixture
def setUp(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    assert login_page.base_url, "BASE_URL is not set"
    yield login_page


@pytest.fixture
def login(setUp, page: Page):
    setUp.login()
    return page


@pytest.fixture
def login_actions(page: Page) -> LoginActions:
    return LoginActions(page)


@pytest.fixture
def quote_actions(page: Page) -> QuoteActions:
    return QuoteActions(page)