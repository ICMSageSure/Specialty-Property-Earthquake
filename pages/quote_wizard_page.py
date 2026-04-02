from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Locator

from .base_page import BasePage


@dataclass
class ApplicantInfo:
    first_name: str
    last_name: str
    phone: str
    email: str


@dataclass
class PropertyInfo:
    address: str
    coverage_limit: str
    year_built: Optional[str] = None
    living_area: Optional[str] = None


class QuoteWizardPage(BasePage):
    """Fields used before reaching quote options."""

    def _address_input(self) -> Locator:
        combobox = self.page.get_by_role("combobox", name="See the best options for")
        if combobox.count() > 0:
            return combobox
        return self.page.locator("#PropertyAddressSingleLine")

    def search_property(self, address: str) -> None:
        address_box = self._address_input()
        address_box.click()
        address_box.fill(address)
        self.page.wait_for_timeout(1000)
        address_box.press("Enter")

    def start_quote(self) -> None:
        self.page.get_by_role("button", name="Start Quote").click()

    def fill_property_details(self, info: PropertyInfo) -> None:
        if info.year_built:
            self.page.get_by_role("textbox", name="Year Built").fill(info.year_built)
        if info.living_area:
            self.page.get_by_role("textbox", name="Living Area").fill(info.living_area)
        coverage_field = self.page.get_by_role(
            "textbox",
            name="Current Companion Insurance Policy Coverage A Dwelling Limit",
        )
        coverage_field.fill(info.coverage_limit)

    def fill_applicant_info(self, applicant: ApplicantInfo) -> None:
        self.page.get_by_role("textbox", name="Primary Applicant First Name").fill(
            applicant.first_name
        )
        self.page.locator("#vm_Applicant_LastName").fill(applicant.last_name)
        self.page.get_by_role("textbox", name="Applicant Phone Number").fill(
            applicant.phone
        )
        self.page.get_by_role("textbox", name="Applicant Email Address").fill(
            applicant.email
        )

    def view_quote_options(self) -> None:
        self.page.get_by_role("button", name="View Quote Options").click()
