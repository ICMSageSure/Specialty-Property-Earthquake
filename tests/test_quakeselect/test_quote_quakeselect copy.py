import pytest
import re
import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
from pages.MGS_LOGIN import Login

relative_path = "uploads/testfile.pdf"

absolute_path = os.path.abspath(relative_path)

load_dotenv()

@pytest.fixture
def setUp(page):
    login = Login(page)
    login.navigate_to_login()
    assert login.url, "BASE_URL is not set"
    yield
    page.close()
    

@pytest.fixture
def login(setUp, page):
    login = Login(page)
    login.enter_username(login.username)
    login.enter_password(login.password)
    return page

def test_quakeselect(page: Page, setUp) -> None:
    base_url = os.getenv("BASE_URL")
    page.goto(base_url)
    
    page.wait_for_selector("text=this is a test")
    page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role("link").click()
    page.get_by_role("treeitem", name="Residential Earthquake Products").locator("span").first.click()
    page.get_by_role("button", name="OK").click()
    page.get_by_role("combobox", name="See the best options for").click()
    page.get_by_role("combobox", name="See the best options for").fill("3 blueb")
    page.wait_for_timeout(1000)
    page.get_by_role("combobox", name="See the best options for").press("ArrowDown")
    page.wait_for_timeout(1000)
    page.get_by_role("combobox", name="See the best options for").press("Enter")
    page.get_by_role("button", name="Start Quote").click()
    page.get_by_role("textbox", name="Year Built").click()
    page.get_by_role("textbox", name="Year Built").fill("2022")
    page.get_by_role("textbox", name="Living Area").click()
    page.get_by_role("textbox", name="Living Area").fill("2022")
    page.get_by_text("+").first.click()
    page.get_by_text("+").nth(1).click()
    page.get_by_text("Residential", exact=True).click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill("600,000")
    page.get_by_role("textbox", name="Primary Applicant First Name").click()
    page.get_by_role("textbox", name="Primary Applicant First Name").fill("ICMTEST")
    page.locator("#vm_Applicant_LastName").click()
    page.locator("#vm_Applicant_LastName").fill("TESTER")
    page.get_by_role("textbox", name="Applicant Phone Number").click()
    page.get_by_role("textbox", name="Applicant Phone Number").fill("7075556789")
    page.get_by_role("textbox", name="Applicant Email Address").click()
    page.get_by_role("textbox", name="Applicant Email Address").fill("ICMGEOTESTER@GMAIL.COM")
    page.get_by_role("button", name="View Quote Options").click()
    expect(page.get_by_label("Review all Eligible Products").get_by_role("paragraph")).to_contain_text("By submitting the request, I understand all eligible products and quotes must be reviewed with the applicant.")
    page.get_by_role("button", name="Agree & Continue").click()
    expect(page.locator("#divSubContent")).to_contain_text("FLEX LIMIT - QUAKE SELECT")
    visible_quote = page.locator('b[data-qs-quotenumber]:not([style*="display:none"])').text_content()
    quote_text = f"Quote: {visible_quote}"
    assert re.fullmatch(r"Quote: QP\d{8}", quote_text), f"Quote format invalid: {quote_text}"
    print(f"\n{quote_text}")
    page.get_by_text("2.5%", exact=True).click()
    expect(page.locator("#divGridNav")).to_contain_text("Dwelling Limit: $600,000")
    expect(page.locator("#divSubContent")).to_contain_text("$600,000")
    page.get_by_role("button", name="Continue Shopping Cart", exact=True).click()
    page.get_by_role("row", name="Yes No Is the dwelling currently under course of construction?").locator("label").first.click()
    page.get_by_role("row", name="Yes No Is the dwelling currently under major renovation affecting habitability?").locator("label").first.click()
    page.get_by_role("row", name="Yes No Does the dwelling have any unrepaired earthquake damage?").locator("label").first.click()
    page.get_by_role("row", name="Yes No Does the dwelling have any log and/or adobe siding?").locator("label").first.click()
    page.get_by_role("row", name="Yes No Is the dwelling located within 500 feet of a high tide beach?").locator("label").first.click()
    page.get_by_role("row", name="Yes No Is the dwelling less").locator("label").first.click()
    page.get_by_role("row", name="Yes No Is any part of the").locator("label").first.click()
    page.get_by_role("button", name="Continue").click()
    expect(page.locator("#divSubContent")).to_contain_text("Property ineligible due to building over water.")
    expect(page.locator("#divSubContent")).to_contain_text("Property ineligible due to unrepaired damage.")
    expect(page.locator("#divSubContent")).to_contain_text("Property ineligible due to the dwelling having any log and/or adobe siding.")
    expect(page.locator("#divSubContent")).to_contain_text("Property ineligible due to dwelling under course of construction or renovation.")
    page.get_by_role("row", name="Yes No Is the dwelling currently under course of construction?").locator("label").nth(1).click()
    page.get_by_role("row", name="Yes No Is the dwelling currently under major renovation affecting habitability?").locator("label").nth(1).click()
    page.get_by_role("row", name="Yes No Does the dwelling have any unrepaired earthquake damage?").locator("label").nth(1).click()
    page.get_by_role("row", name="Yes No Does the dwelling have any log and/or adobe siding?").locator("label").nth(1).click()
    page.get_by_role("row", name="Yes No Is the dwelling located within 500 feet of a high tide beach?").locator("label").nth(1).click()
    page.get_by_role("row", name="Yes No Is the dwelling less").locator("label").nth(1).click()
    page.get_by_role("row", name="Yes No Is any part of the").locator("label").nth(1).click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Pay Now").click()
    page.get_by_text("Applicant", exact=True).click()
    page.get_by_text("Full Pay$").click()
    page.get_by_text("Auto Pay On").click()
    page.set_input_files("#fileHODec",
                        absolute_path)
    page.locator(".eqq-terms-and-conditions-agreement > .eqq-checkbox-container > .eqq-checkbox > .bho-checkbox > .bho-checkmark").click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("link", name="Add new payment method").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter card number").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter card number").press_sequentially("4111 1111 1111 1111")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_text("Expiration Date").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Expiration Date").fill("11/26")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_text("Name on card").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter name as it").fill("icmtest")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_text("Billing Address").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_placeholder("Please, enter billing address").fill("1455 oliver rd")
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_placeholder("Billing Zip").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_placeholder("Billing Zip").fill("94534")
    page.get_by_role("dialog", name="Payment method").content_frame.locator("gm2-action-buttons-control").filter(has_text="Submit Cancel").locator("div").nth(1).click()
