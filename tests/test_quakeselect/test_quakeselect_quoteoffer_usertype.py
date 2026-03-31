# test_quakeselect_quoteoffer_usertype.py
# Supports login as either an "agent" or "internal_user".
# Set USER_TYPE env var to "agent" (default) or "internal_user".
#
# Agent credentials:    AGENT_USERNAME    / AGENT_PASSWORD    (defaults: BRK99102 / Password1)
# Internal credentials: INTERNAL_USERNAME / INTERNAL_PASSWORD (defaults: USERNAME / PASSWORD from .env)

import pytest
import re
import os
import csv
import random
from datetime import datetime
from playwright.sync_api import Page, expect
from dotenv import load_dotenv

load_dotenv()

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
    "2102 Harborview Ct, Santa Cruz, CA 95062",
]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width": 1920, "height": 1080}, "ignore_https_errors": True}


@pytest.mark.parametrize("auto_payment,payment_plan", [
    ("Auto Pay On",  "Full Pay"),
    ("Auto Pay On",  "Three Pay"),
    ("Auto Pay On",  "Four Pay"),
    ("Auto Pay On",  "Monthly Pay"),
    ("Auto Pay Off", "Full Pay"),
    ("Auto Pay Off", "Three Pay"),
    ("Auto Pay Off", "Four Pay"),
    ("Auto Pay Off", "Monthly Pay"),
])
def test_quakeselect_quoteoffer_usertype(page: Page, auto_payment: str, payment_plan: str) -> None:
    # ── User type configuration ──────────────────────────────────────────────
    user_type = os.getenv("USER_TYPE", "agent")  # "agent" or "internal_user"

    if user_type == "agent":
        username = os.getenv("AGENT_USERNAME", "BRK99102")
        password = os.getenv("AGENT_PASSWORD", "Password1")
    elif user_type == "internal_user":
        username = os.getenv("INTERNAL_USERNAME", os.getenv("USERNAME", ""))
        password = os.getenv("INTERNAL_PASSWORD", os.getenv("PASSWORD", "Password1"))
    else:
        raise ValueError(f"Unknown USER_TYPE: '{user_type}'. Expected 'agent' or 'internal_user'.")

    print(f"\nLogging in as {user_type}: {username}")

    # ── Login ────────────────────────────────────────────────────────────────
    page.goto("https://tst.mygeosource.com/")
    page.get_by_role("textbox", name="Policyholder Email or Agent").fill(username)
    page.get_by_role("textbox", name="Password").fill(password)
    page.get_by_role("button", name="Log In", exact=True).click()
    page.wait_for_selector("text=Hello,")

    # ── Start new quote ──────────────────────────────────────────────────────
    page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role("link").click()
    page.get_by_role("treeitem", name="Residential Earthquake Products").locator("span").first.click()
    page.get_by_role("button", name="OK").click()

    # ── Address entry ────────────────────────────────────────────────────────
    address = random.choice(address_list)
    print(f"\nUsing address: {address}")
    address_box = page.get_by_role("combobox", name="See the best options for")
    address_box.press_sequentially(address, delay=50)
    page.wait_for_timeout(2000)
    address_box.press("Enter")
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Start Quote").click()

    # ── Property details (only visible for some addresses) ───────────────────
    if page.get_by_role("textbox", name="Year Built").is_visible():
        page.get_by_role("textbox", name="Year Built").click()
        page.get_by_role("textbox", name="Year Built").fill("2022")
        page.get_by_role("textbox", name="Living Area").click()
        page.get_by_role("textbox", name="Living Area").fill("2022")
    page.get_by_text("+").first.click()
    page.get_by_text("+").nth(1).click()
    page.get_by_text("Residential", exact=True).click()

    # ── Applicant information ────────────────────────────────────────────────
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill("600,000")
    page.get_by_role("textbox", name="Primary Applicant First Name").fill("ICMTEST")
    page.locator("#vm_Applicant_LastName").fill("TESTER")
    page.get_by_role("textbox", name="Applicant Phone Number").fill("7075556789")
    page.get_by_role("textbox", name="Applicant Email Address").fill("ICMGEOTESTER+1020@GMAIL.COM")

    # ── Quote options ────────────────────────────────────────────────────────
    page.get_by_role("button", name="View Quote Options").click()
    expect(page.get_by_label("Review all Eligible Products").get_by_role("paragraph")).to_contain_text(
        "By submitting the request, I understand all eligible products and quotes must be reviewed with the applicant."
    )
    page.get_by_role("button", name="Agree & Continue").click()
    expect(page.locator("#divSubContent")).to_contain_text("FLEX LIMIT - QUAKE SELECT")

    visible_quote = page.locator('b[data-qs-quotenumber]:not([style*="display:none"])').text_content()
    quote_text = f"Quote: {visible_quote}"
    assert re.fullmatch(r"Quote: QP\d{8}", quote_text), f"Quote format invalid: {quote_text}"
    print(f"\n{quote_text}")

    page.get_by_text("2.5%", exact=True).click()
    expect(page.locator("#divGridNav")).to_contain_text("Dwelling Limit: $600,000")
    expect(page.locator("#divSubContent")).to_contain_text("$600,000")

    # ── Capture quote details ─────────────────────────────────────────────────
    grid_nav_text = page.locator("#divGridNav").text_content() or ""
    sub_content_text = page.locator("#divSubContent").text_content() or ""

    # Dwelling limit from grid nav
    dwelling_match = re.search(r"Dwelling Limit:\s*(\$[\d,]+)", grid_nav_text)
    dwelling_value = dwelling_match.group(1) if dwelling_match else "$600,000"

    # Premium — first "Annual Premium" after the selected quote number in the page text
    quote_pos = sub_content_text.find(visible_quote)
    premium_match = re.search(r"(\$[\d,]+\.\d{2})\s+Annual Premium", sub_content_text[quote_pos:]) if quote_pos != -1 else None
    premium_value = premium_match.group(1) if premium_match else "N/A"

    product_name = "FLEX LIMIT - QUAKE SELECT"
    deductible = "2.5%"
    effective_date = "N/A"  # captured from enrollment page below

    # ── Continue to enrollment ────────────────────────────────────────────────
    page.get_by_role("button", name="Continue Shopping Cart", exact=True).click()
    page.get_by_role("button", name="Continue").click()
    page.get_by_role("button", name="Finalize Application").click()
    page.get_by_text("Applicant", exact=True).click()

    # ── Payment plan (final enrollment screen) ────────────────────────────────
    payment_toolbar = page.locator(".radio-toolbar").filter(has_text="Full Pay")
    payment_option = payment_toolbar.locator(".radio-item").filter(has_text=payment_plan).first
    if not payment_option.is_visible():
        print(f"\nPayment plan '{payment_plan}' not available — skipping.")
        return
    payment_option.click()

    # Auto pay toggle is hidden for Monthly Pay
    auto_pay_btn = page.get_by_text(auto_payment, exact=True).first
    if auto_pay_btn.is_visible():
        auto_pay_btn.click()
    else:
        print(f"\nAuto pay toggle not visible for '{payment_plan}' — skipping.")
    page.locator(".eqq-terms-and-conditions-agreement > .eqq-checkbox-container > .eqq-checkbox > .bho-checkbox > .bho-checkmark").click()
    # ── Capture effective date from enrollment summary page ───────────────────
    effective_date = page.locator("#EffectiveDate").input_value() or "N/A"

    print(f"\nProduct:        {product_name}")
    print(f"Quote Number:   {visible_quote}")
    print(f"Deductible:     {deductible}")
    print(f"Dwelling Limit: {dwelling_value}")
    print(f"Premium:        {premium_value}")
    print(f"Effective Date: {effective_date}")

    page.get_by_role("button", name="Continue").click()

    
    # ── Export results to CSV ─────────────────────────────────────────────────
    csv_path = os.path.abspath("quote_results.csv")
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "User Type", "Username", "Address", "Product", "Quote Number", "Deductible", "Dwelling Limit", "Premium", "Payment Plan", "Auto Pay", "Effective Date"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_type, username, address, product_name, visible_quote, deductible, dwelling_value, premium_value, payment_plan, auto_payment, effective_date])
    print(f"\nResults exported to: {csv_path}")
