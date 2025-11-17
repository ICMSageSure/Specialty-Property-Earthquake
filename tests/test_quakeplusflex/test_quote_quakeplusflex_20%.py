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
    page.get_by_role("textbox", name="Policyholder Email or Agent").click()
    page.get_by_role("textbox", name="Policyholder Email or Agent").fill("brk99102")
    page.get_by_text("Password", exact=True).click()
    page.get_by_role("textbox", name="Password").fill("Password1")
    page.get_by_role("button", name="Log In", exact=True).click()
    page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role("link").click()
    page.get_by_role("treeitem", name="Residential Earthquake Products").locator("span").first.click()
    page.get_by_role("button", name="OK").click()
    page.get_by_role("combobox", name="See the best options for").fill("3424 hidden vall")
    page.get_by_text("3424 Hidden Valley Ln,").click()
    page.get_by_role("button", name="Start Quote").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill("360,0000")
    page.get_by_role("button", name="View Quote Options").click()
    page.get_by_role("button", name="Agree & Continue").click()
    # page.get_by_role("link", name="Expand All").click()
    page.get_by_text("20%", exact=True).click()
    page.get_by_role("button", name="Continue Shopping Cart").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Finalize Application").click()
    page.get_by_role("textbox", name="Primary Applicant First Name").click()
    page.get_by_role("textbox", name="Primary Applicant First Name").fill("icmtest")
    page.get_by_role("textbox", name="Last Name").click()
    page.get_by_role("textbox", name="Last Name").fill("tester")
    page.get_by_role("textbox", name="Primary Phone").click()
    page.get_by_role("textbox", name="Primary Phone").fill("7075551234")
    page.get_by_role("textbox", name="Email Address", exact=True).click()
    page.get_by_role("textbox", name="Email Address", exact=True).fill("icmgeotester@gmail.com")
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
    td_text = page.locator('table.eqq-summary td').first.text_content()
    match = re.fullmatch(r"UU\d{8}", td_text.strip())
    print(f"Quote Number: \n {td_text.strip()}")
    page.wait_for_timeout(5000)