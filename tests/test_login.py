import pytest
import os
from playwright.sync_api import sync_playwright
from pages.MGS_LOGIN import Login

@pytest.fixture
def setUp(page):
    login = Login(page)
    login.navigate_to_login()
    assert login.url, "BASE_URL is not set"
    yield
    page.close()
    


@pytest.fixture
def login(setUp, page):
    login = Login(page)
    login.enter_username(login.username)
    login.enter_password(login.password)
    return page

def test_happypath_login(login):
    page = login