from __future__ import annotations

from playwright.sync_api import Locator, Page


class BasePage:
    """Base helper with a shared Playwright page handle."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def wait_for_dom(self) -> None:
        self.page.wait_for_load_state("domcontentloaded")

    def wait_for_network_idle(self) -> None:
        self.page.wait_for_load_state("networkidle")

    def get_locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def screenshot(self, path: str) -> None:
        self.page.screenshot(path=path, full_page=True)
