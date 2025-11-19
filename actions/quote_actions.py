from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, Optional

from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from pages.finalize_application_page import (
    AddressInfo,
    EntityInfo,
    FinalizeApplicationPage,
)
from pages.payment_modal import PaymentDetails, PaymentModal
from pages.quote_options_page import QuoteOptionsPage
from pages.quote_wizard_page import ApplicantInfo, PropertyInfo, QuoteWizardPage
from pages.shopping_cart_page import ShoppingCartPage

from .login_actions import LoginActions


@dataclass
class QuotePreferences:
    deductible: str = "10%"
    applicant_type: str = "Individual"
    bill_to: str = "Applicant"
    payment_plan: str = "Full Pay$"
    auto_pay: str = "Auto Pay On"
    documents: Dict[str, str] = field(default_factory=dict)


class QuoteActions:
    """Glue layer that stitches page objects together for common flows."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_actions = LoginActions(page)
        self.dashboard = DashboardPage(page)
        self.quote_wizard = QuoteWizardPage(page)
        self.quote_options = QuoteOptionsPage(page)
        self.shopping_cart = ShoppingCartPage(page)
        self.finalize_page = FinalizeApplicationPage(page)
        self.payment_modal = PaymentModal(page)

    def _resolve_property_info(self, property_info: Optional[PropertyInfo]) -> PropertyInfo:
        if property_info:
            return property_info
        default_address = os.getenv(
            "DEFAULT_PROPERTY_ADDRESS",
            "3424 Hidden Valley Ln, Fairfield, CA 94534",
        )
        coverage_limit = os.getenv("DEFAULT_COVERAGE_LIMIT", "600000")
        return PropertyInfo(address=default_address, coverage_limit=coverage_limit)

    def _resolve_applicant_info(self, applicant_info: Optional[ApplicantInfo]) -> ApplicantInfo:
        if applicant_info:
            return applicant_info
        return ApplicantInfo(
            first_name=os.getenv("APPLICANT_FIRST_NAME", "ICMTEST"),
            last_name=os.getenv("APPLICANT_LAST_NAME", "TESTER"),
            phone=os.getenv("APPLICANT_PHONE", "7075551234"),
            email=os.getenv("APPLICANT_EMAIL", "ICMGEOTESTER@GMAIL.COM"),
        )

    def login_and_launch_quote(self) -> None:
        self.login_actions.login()
        self.dashboard.wait_for_ready()
        self.dashboard.start_residential_earthquake_quote()

    def complete_quote_wizard(
        self,
        property_info: Optional[PropertyInfo],
        applicant_info: Optional[ApplicantInfo],
    ) -> None:
        property_info = self._resolve_property_info(property_info)
        applicant_info = self._resolve_applicant_info(applicant_info)
        self.quote_wizard.search_property(property_info.address)
        self.quote_wizard.start_quote()
        self.quote_wizard.fill_property_details(property_info)
        self.quote_wizard.fill_applicant_info(applicant_info)
        self.quote_wizard.view_quote_options()

    def configure_quote_options(self, preferences: QuotePreferences) -> Optional[str]:
        self.quote_options.agree_and_continue()
        self.quote_options.wait_for_quote_grid()
        quote_number = self.quote_options.capture_quote_number()
        self.quote_options.select_deductible(preferences.deductible)
        self.quote_options.continue_to_shopping_cart()
        self.quote_options.continue_to_underwriting()
        return quote_number

    def answer_underwriting(self) -> None:
        self.shopping_cart.answer_questions("No")
        self.shopping_cart.continue_to_finalize()

    def finalize_application(
        self,
        preferences: QuotePreferences,
        entity_info: Optional[EntityInfo] = None,
        billing_address: Optional[AddressInfo] = None,
        payment_details: Optional[PaymentDetails] = None,
    ) -> None:
        self.finalize_page.click_finalize_application()
        self.finalize_page.select_applicant_type(preferences.applicant_type, entity_info)
        self.finalize_page.select_bill_to(preferences.bill_to, billing_address)
        self.finalize_page.select_payment_plan(preferences.payment_plan)
        self.finalize_page.toggle_auto_pay(preferences.auto_pay)
        if preferences.documents:
            self.finalize_page.upload_documents(preferences.documents)
        self.finalize_page.accept_terms()
        self.finalize_page.click_pay_now()
        if payment_details:
            self.payment_modal.add_payment_method(payment_details)

    def build_quakeplusflex_quote(
        self,
        property_info: Optional[PropertyInfo] = None,
        applicant_info: Optional[ApplicantInfo] = None,
        preferences: Optional[QuotePreferences] = None,
        entity_info: Optional[EntityInfo] = None,
        billing_address: Optional[AddressInfo] = None,
        payment_details: Optional[PaymentDetails] = None,
    ) -> Optional[str]:
        quote_preferences = preferences or QuotePreferences()
        self.login_and_launch_quote()
        self.complete_quote_wizard(property_info, applicant_info)
        quote_number = self.configure_quote_options(quote_preferences)
        self.answer_underwriting()
        self.finalize_application(
            quote_preferences,
            entity_info=entity_info,
            billing_address=billing_address,
            payment_details=payment_details,
        )
        return quote_number


__all__ = [
    "QuoteActions",
    "QuotePreferences",
    "ApplicantInfo",
    "PropertyInfo",
    "EntityInfo",
    "AddressInfo",
    "PaymentDetails",
]
