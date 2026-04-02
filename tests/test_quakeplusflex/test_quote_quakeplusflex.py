import os
import re

import pytest

from actions import (
    QuoteActions,
    QuotePreferences,
    ApplicantInfo,
    PropertyInfo,
    EntityInfo,
    AddressInfo,
    PaymentDetails,
)


def _abs(path: str) -> str:
    return os.path.abspath(path)


@pytest.mark.e2e
def test_quakeplusflex_end_to_end(quote_actions: QuoteActions) -> None:
    """Happy-path QuakePlusFlex quote that exercises the shared POM/actions."""

    property_info = PropertyInfo(
        address=os.getenv(
            "TEST_ADDRESS", "3424 Hidden Valley Ln, Fairfield, CA 94534"
        ),
        coverage_limit=os.getenv("COVERAGE_LIMIT", "4,600,000"),
    )

    applicant = ApplicantInfo(
        first_name=os.getenv("APPLICANT_FIRST_NAME", "ICMTEST"),
        last_name=os.getenv("APPLICANT_LAST_NAME", "TESTER"),
        phone=os.getenv("APPLICANT_PHONE", "7075551234"),
        email=os.getenv("APPLICANT_EMAIL", "ICMGEOTESTER@GMAIL.COM"),
    )

    preferences = QuotePreferences(
        deductible=os.getenv("DEDUCTIBLE_PERCENT", "10%"),
        applicant_type=os.getenv("APPLICANT_TYPE", "LLC"),
        bill_to=os.getenv("BILL_TO", "Alternate Payor"),
        payment_plan=os.getenv("PAYMENT_PLAN", "Three Pay$"),
        auto_pay=os.getenv("AUTO_PAYMENT", "Auto Pay On"),
        documents={
            "#fileD1": _abs("uploads/testfile.pdf"),
            "#fileSL2": _abs("uploads/testfile2.pdf"),
            "#fileHODec": _abs("uploads/testfile3.pdf"),
        },
    )

    entity_info = (
        EntityInfo(
            entity_name=os.getenv("ENTITY_NAME", "ICMTEST ENTITYLLC"),
            manager_first_name=os.getenv("ENTITY_MANAGER_FIRST", "LLC ICMFIRSTNAME"),
            manager_last_name=os.getenv("ENTITY_MANAGER_LAST", "ICMLASTNAME"),
        )
        if preferences.applicant_type in {"LLC", "Trust", "Estate", "Corporation"}
        else None
    )

    billing_address = (
        AddressInfo(
            addressee1=os.getenv("BILL_TO_NAME", "ICMTEST BILLING"),
            street=os.getenv("BILL_TO_STREET", "1455 ALTERNATE RD"),
            city=os.getenv("BILL_TO_CITY", "FAIRFIELD"),
            state=os.getenv("BILL_TO_STATE", "CA"),
            zip_code=os.getenv("BILL_TO_ZIP", "94534"),
            loan_number=os.getenv("BILL_TO_LOAN", "11223344"),
        )
        if preferences.bill_to in {"Alternate Payor", "Mortgagee"}
        else None
    )

    payment = PaymentDetails(
        card_number=os.getenv("TEST_CARD_NUMBER", "4111111111111111"),
        expiration_date=os.getenv("TEST_CARD_EXPIRATION", "11/26"),
        name_on_card=os.getenv("TEST_CARD_NAME", "ICM TEST"),
        billing_address=os.getenv("TEST_CARD_ADDRESS", "1455 Oliver Rd"),
        billing_zip=os.getenv("TEST_CARD_ZIP", "94534"),
    )

    quote_number = quote_actions.build_quakeplusflex_quote(
        property_info=property_info,
        applicant_info=applicant,
        preferences=preferences,
        entity_info=entity_info,
        billing_address=billing_address,
        payment_details=payment,
    )

    assert quote_number, "Quote number was not captured"
    assert re.fullmatch(r"QP\d{8}", quote_number), f"Unexpected quote: {quote_number}"
