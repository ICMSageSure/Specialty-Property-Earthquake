from __future__ import annotations

from typing import Iterable

from .base_page import BasePage


QUESTION_ROWS: Iterable[str] = [
    "Yes No Is the dwelling currently under course of construction?",
    "Yes No Is the dwelling currently under major renovation affecting habitability?",
    "Yes No Does the dwelling have any unrepaired earthquake damage?",
    "Yes No Does the dwelling have any log and/or adobe siding?",
    "Yes No Is the dwelling located within 500 feet of a high tide beach?",
    "Yes No Is the dwelling less",
    "Yes No Is any part of the",
]


class ShoppingCartPage(BasePage):
    """Underwriting questions + progression buttons."""

    def continue_from_quote_options(self) -> None:
        self.page.get_by_role("button", name="Continue Shopping Cart", exact=True).click()

    def answer_questions(self, answer: str = "No") -> None:
        for row_name in QUESTION_ROWS:
            row = self.page.get_by_role("row", name=row_name)
            if answer.lower().startswith("y"):
                row.locator("label").first.click()
            else:
                row.locator("label").nth(1).click()

    def continue_to_finalize(self) -> None:
        self.page.get_by_role("button", name="Continue").click()
