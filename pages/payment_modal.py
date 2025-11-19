from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from playwright.sync_api import Frame

from .base_page import BasePage


@dataclass
class PaymentDetails:
    card_number: str
    expiration_date: str
    name_on_card: str
    billing_address: str
    billing_zip: str


class PaymentModal(BasePage):
    """Interact with the payment iframe."""

    def _frame(self) -> Optional[Frame]:
        dialog = self.page.get_by_role("dialog", name="Payment method")
        return dialog.content_frame

    def add_payment_method(self, details: PaymentDetails) -> None:
        frame = self._frame()
        if frame is None:
            raise RuntimeError("Payment method frame is not visible.")
        frame.get_by_role("link", name="Add new payment method").click()
        frame.get_by_role("textbox", name="Please, enter card number").fill(
            details.card_number
        )
        frame.get_by_role("textbox", name="Expiration Date").fill(details.expiration_date)
        frame.get_by_role("textbox", name="Please, enter name as it").fill(
            details.name_on_card
        )
        frame.get_by_placeholder("Please, enter billing address").fill(
            details.billing_address
        )
        frame.get_by_placeholder("Billing Zip").fill(details.billing_zip)
        frame.locator("gm2-action-buttons-control").filter(
            has_text="Submit Cancel"
        ).locator("div").nth(1).click()
