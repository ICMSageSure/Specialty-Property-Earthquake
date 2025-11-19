from __future__ import annotations

from playwright.sync_api import expect

from .base_page import BasePage


class DashboardPage(BasePage):
    """Interactions on the landing page after login."""

    def wait_for_ready(self) -> None:
        expect(
            self.page.get_by_role("paragraph").filter(has_text="Start New Quote")
        ).to_be_visible()

    def open_start_new_quote(self) -> None:
        self.page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role(
            "link"
        ).click()

    def choose_residential_earthquake_products(self) -> None:
        self.page.locator('[id="optionResidential\\ Earthquake"]').get_by_text(
            "Residential Earthquake Products"
        ).click()
        self.page.get_by_role("button", name="OK").click()

    def start_residential_earthquake_quote(self) -> None:
        self.open_start_new_quote()
        self.choose_residential_earthquake_products()
