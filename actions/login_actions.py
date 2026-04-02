from __future__ import annotations

from typing import Optional

from playwright.sync_api import Page

from pages.login_page import LoginPage


class LoginActions:
    """High-level steps for authentication."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_page = LoginPage(page)

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        self.login_page.open()
        self.login_page.login(username=username, password=password)
