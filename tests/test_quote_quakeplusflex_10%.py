# this test case will generate a quote for QuakePlusFlex 5% deductible with Full Pay and Auto Pay On

import re
from playwright.sync_api import Page, expect
import os
import pytest
import random

relative_path1 = "uploads/testfile.pdf"
relative_path2 = "uploads/testfile2.pdf"
relative_path3 = "uploads/testfile3.pdf"

absolute_path1 = os.path.abspath(relative_path1)
absolute_path2 = os.path.abspath(relative_path2)
absolute_path3 = os.path.abspath(relative_path3)

address_list = [
    "59 Ventana Dr, American Canyon, CA 94503",
    "2861 Pinnacles Ter, Fremont, CA 94538",
    "1196 Sunny Ct, San Jose, CA 95116",
    "4088 E Heritage Ln, Ontario, CA 91761",
    "2182 Esperanca Ave, Santa Clara, CA 95054",
    "1955 Celeste Ave, Clovis, CA 93611",
    "620 Tanbark Oak Ct, El Dorado Hills, CA 95762",
    "2725 Lake St, Bakersfield, CA 93306",
    "329 Beaumont Blvd, Pacifica, CA 94044",
    "735 The Alameda, El Granada, CA 94018",
    "2102 Harborview Ct, Santa Cruz, CA 95062"
]

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width":1920,"height":1080}}

def test_quote_quakeplusflex_5percent(page: Page) -> None:
    page.goto("https://tst.mygeosource.com/")
    page.get_by_role("textbox", name="Policyholder Email or Agent").fill("BRK99102")
    page.get_by_role("textbox", name="Password").fill("Password1")
    page.get_by_role("button", name="Log In", exact=True).click()
    page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role("link").click()
    page.locator("[id=\"optionResidential\\ Earthquake\"]").get_by_text("Residential Earthquake Products").click()
    page.get_by_role("button", name="OK").click()
    page.get_by_role("combobox", name="See the best options for").click()
    page.get_by_role("combobox", name="See the best options for").fill(random.choice(address_list))
    page.wait_for_timeout(1000)
    page.get_by_role("combobox", name="See the best options for").press("Enter")
    page.get_by_role("button", name="Start Quote").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill("3600000")
    page.get_by_role("textbox", name="Primary Applicant First Name").click()
    page.get_by_role("textbox", name="Primary Applicant First Name").press("CapsLock")
    page.get_by_role("textbox", name="Primary Applicant First Name").fill("ICMTEST")
    page.locator("#vm_Applicant_LastName").click()
    page.locator("#vm_Applicant_LastName").fill("TESTER")
    page.get_by_role("textbox", name="Applicant Phone Number").click()
    page.get_by_role("textbox", name="Applicant Phone Number").fill("7075551234")
    page.get_by_role("textbox", name="Applicant Email Address").click()
    page.get_by_role("textbox", name="Applicant Email Address").fill("ICMGEOTESTER@GMAIL.COM")
    page.get_by_role("button", name="View Quote Options").click()
    page.get_by_role("button", name="Agree & Continue").click()
    page.locator("#lnkExpandAll").click()
    page.get_by_text("10%", exact=True).click()
    page.get_by_role("button", name="Continue Shopping Cart", exact=True).click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Pay Now").click()
    page.get_by_text("Applicant", exact=True).click()
    payment_type = page.get_by_text("Full Pay$")
    payment_type.click()
    print(f"\nSelected Payment Type: {payment_type.inner_text()}")
    auto_pay_onoff = page.get_by_text("Auto Pay On")
    auto_pay_onoff.click()
    print(f"Selected Auto Pay: {auto_pay_onoff.inner_text()}")
    page.set_input_files("#fileD1",
                    absolute_path1)
    page.set_input_files("#fileSL2",
                absolute_path2)
    page.set_input_files("#fileHODec",
                absolute_path3)
    page.locator(".eqq-terms-and-conditions-agreement > .eqq-checkbox-container > .eqq-checkbox > .bho-checkbox > .bho-checkmark").click()
    td_text = page.locator('table.eqq-summary td').first.text_content()
    match = re.fullmatch(r"UU\d{8}", td_text.strip())
    print(f"Quote Number:\n {td_text.strip()}")
    payment_toolbar = page.locator('.radio-toolbar').filter(has_text="Full Pay")
    radio_items = payment_toolbar.locator('.radio-item')
    for i in range(radio_items.count()):
        label_text = radio_items.nth(i).locator('label').inner_text().split('\n')
        if len(label_text) == 2:
            plan, amount = label_text
            if plan.strip() in ["Full Pay", "Three Pay", "Monthly Pay"]:
                print(f"{plan.strip()}: {amount.strip()}")
        else:
            print(f"Unknown format: {label_text}")
    screenshot_path = "screenshot_quote.png"
    page.screenshot(path=screenshot_path, full_page=True)
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("link", name="Add new payment method").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Expiration Date").fill("11/26")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter card number").fill("4111 1111 1111 1111")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter name as it").fill("ICMTEST TESTER")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_placeholder("Please, enter billing address").fill("1455 OLIVER RD")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_placeholder("Billing Zip").fill("94534")
    page.wait_for_timeout(5000)