from __future__ import annotations

from typing import Optional

from playwright.sync_api import expect

from .base_page import BasePage


DEDUCTIBLE_LOCATORS = {
    "10%": "label[for=rdoFullDeductibleList_SLEQFL0]",
    "15%": "label[for=rdoFullDeductibleList_SLEQFL1]",
    "20%": "label[for=rdoFullDeductibleList_SLEQFL2]",
    "25%": "label[for=rdoFullDeductibleList_SLEQFL3]",
}


class QuoteOptionsPage(BasePage):
    """Interactions after the quote options modal shows up."""

    def agree_and_continue(self) -> None:
        self.page.get_by_role("button", name="Agree & Continue").click()

    def wait_for_quote_grid(self) -> None:
        expect(self.page.locator("#divSubContent")).to_be_visible()

    def select_deductible(self, label: str) -> None:
        locator = DEDUCTIBLE_LOCATORS.get(label)
        if locator:
            self.page.locator(locator).click()
        else:
            self.page.get_by_text(label, exact=True).click()

    def continue_to_shopping_cart(self) -> None:
        self.page.get_by_role("button", name="Continue Shopping Cart", exact=True).click()

    def continue_to_underwriting(self) -> None:
        continue_buttons = self.page.get_by_role("button", name="Continue")
        if continue_buttons.count() > 1:
            continue_buttons.nth(1).click()
        else:
            continue_buttons.first.click()

    def capture_quote_number(self) -> Optional[str]:
        locator = self.page.locator('b[data-qs-quotenumber]:not([style*="display:none"])')
        if locator.count() == 0:
            return None
        quote = locator.first.text_content() or ""
        return quote.strip()
