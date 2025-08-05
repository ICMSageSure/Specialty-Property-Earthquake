import re
from playwright.sync_api import Page, expect
import os
import pytest

relative_path1 = "uploads/testfile.pdf"
relative_path2 = "uploads/testfile2.pdf"
relative_path3 = "uploads/testfile3.pdf"

absolute_path1 = os.path.abspath(relative_path1)
absolute_path2 = os.path.abspath(relative_path2)
absolute_path3 = os.path.abspath(relative_path3)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width":1920,"height":1080}}

def test_example(page: Page) -> None:
    page.goto("https://tst.mygeosource.com/")
    page.get_by_role("textbox", name="Policyholder Email or Agent").fill("BRK99102")
    page.get_by_role("textbox", name="Password").fill("Password1")
    page.get_by_role("button", name="Log In", exact=True).click()
    page.goto("https://tst.mygeosource.com/Dashboard/MyAccount/Home")
    page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role("link").click()
    page.locator("[id=\"optionResidential\\ Earthquake\"]").get_by_text("Residential Earthquake Products").click()
    page.get_by_role("button", name="OK").click()
    page.goto("https://tst.mygeosource.com/EQQ/Quoting/PropertyAddress")
    page.get_by_role("combobox", name="See the best options for").click()
    page.get_by_role("combobox", name="See the best options for").fill("3424 Hidden Valley Ln")
    page.wait_for_timeout(1000)
    # page.get_by_role("combobox", name="See the best options for").press("ArrowDown")
    # page.wait_for_timeout(1000)
    page.get_by_role("combobox", name="See the best options for").press("Enter")
    page.get_by_role("button", name="Start Quote").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill("350,0000")
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
    page.goto("https://tst.mygeosource.com/EQQ/Quoting/QuoteOptions2")
    page.get_by_role("button", name="Agree & Continue").click()
    page.get_by_role("img", name="expand").nth(1).click()
    page.get_by_role("button", name="Continue Shopping Cart").nth(1).click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Pay Now").click()
    page.get_by_text("Applicant", exact=True).click()
    page.get_by_text("Full Pay$").click()
    page.get_by_text("Auto Pay On").click()
    page.set_input_files("#fileD1",
                    absolute_path1)
    page.set_input_files("#fileSL2",
                absolute_path2)
    page.set_input_files("#fileHODec",
                absolute_path3)
    page.locator(".eqq-terms-and-conditions-agreement > .eqq-checkbox-container > .eqq-checkbox > .bho-checkbox > .bho-checkmark").click()
    page.wait_for_timeout(5000)