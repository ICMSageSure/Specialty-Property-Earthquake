from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from playwright.sync_api import expect

from .base_page import BasePage

load_dotenv()


class LoginPage(BasePage):
    """Page object that encapsulates authentication helpers."""

    def __init__(self, page, base_url: Optional[str] = None) -> None:
        super().__init__(page)
        self.base_url = base_url or os.getenv("BASE_URL")
        self._default_username = os.getenv("USERNAME")
        self._default_password = os.getenv("PASSWORD")

    def open(self) -> "LoginPage":
        if not self.base_url:
            raise RuntimeError("BASE_URL is not configured in the environment.")
        self.page.goto(self.base_url)
        self.wait_for_dom()
        expect(
            self.page.get_by_role("textbox", name="Policyholder Email or Agent")
        ).to_be_visible()
        return self

    def fill_username(self, username: str) -> None:
        self.page.get_by_role("textbox", name="Policyholder Email or Agent").fill(
            username
        )

    def fill_password(self, password: str) -> None:
        self.page.get_by_role("textbox", name="Password").fill(password)

    def submit(self) -> None:
        self.page.get_by_role("button", name="Log In", exact=True).click()
        self.wait_for_network_idle()

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        username = username or self._default_username
        password = password or self._default_password
        if not username or not password:
            raise ValueError(
                "Username and password are required. Set USERNAME/PASSWORD env vars or pass values explicitly."
            )
        self.fill_username(username)
        self.fill_password(password)
        self.submit()
