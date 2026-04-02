from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from .base_page import BasePage


@dataclass
class EntityInfo:
    entity_name: str
    manager_first_name: str
    manager_last_name: str


@dataclass
class AddressInfo:
    addressee1: str
    street: str
    city: str
    state: str
    zip_code: str
    loan_number: Optional[str] = None


class FinalizeApplicationPage(BasePage):
    """Handles finalize application + billing steps."""

    def click_finalize_application(self) -> None:
        self.page.get_by_role("button", name="Finalize Application").click()

    def select_applicant_type(self, applicant_type: str, entity: Optional[EntityInfo] = None) -> None:
        toolbar = self.page.locator(".radio-toolbar").nth(0)
        toolbar.get_by_text(applicant_type, exact=True).click()
        if entity:
            self.page.locator("#Entity").fill(entity.entity_name)
            self.page.locator("#ManagingMember_FirstName").fill(entity.manager_first_name)
            self.page.locator("#ManagingMember_LastName").fill(entity.manager_last_name)

    def select_bill_to(self, choice: str, address: Optional[AddressInfo] = None) -> None:
        self.page.get_by_text(choice, exact=True).click()
        if not address:
            return
        if choice == "Alternate Payor":
            self.page.locator("#AlternatePayor_Addressee1").fill(address.addressee1)
            self.page.locator("#AlternatePayor_Street").fill(address.street)
            self.page.locator("#AlternatePayor_City").fill(address.city)
            self.page.locator("#AlternatePayor_State").select_option(address.state)
            self.page.locator("#AlternatePayor_ZipCode").fill(address.zip_code)
            if address.loan_number:
                self.page.locator("#AlternatePayorLoanNumber").fill(address.loan_number)
        elif choice == "Mortgagee":
            self.page.locator("#btn-edit-mortgagee").click()
            self.page.locator("#Mortgagee1_Addressee1").fill(address.addressee1)
            self.page.locator("#Mortgagee1_Street").fill(address.street)
            self.page.locator("#Mortgagee1_City").fill(address.city)
            self.page.locator("#Mortgagee1_State").select_option(address.state)
            self.page.locator("#Mortgagee1_ZipCode").fill(address.zip_code)
            if address.loan_number:
                self.page.locator("#Mortgagee1LoanNumber").fill(address.loan_number)

    def select_payment_plan(self, plan_label: str) -> None:
        self.page.get_by_text(plan_label, exact=True).click()

    def toggle_auto_pay(self, option_label: str) -> None:
        self.page.get_by_text(option_label, exact=True).click()

    def upload_documents(self, documents: Dict[str, str]) -> None:
        for locator, file_path in documents.items():
            self.page.set_input_files(locator, file_path)

    def accept_terms(self) -> None:
        self.page.locator(
            ".eqq-terms-and-conditions-agreement .eqq-checkbox .bho-checkmark"
        ).click()

    def click_pay_now(self) -> None:
        self.page.get_by_role("button", name="Pay Now").click()
