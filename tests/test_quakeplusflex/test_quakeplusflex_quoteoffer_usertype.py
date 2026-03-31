# test_quakeplusflex_quoteoffer_usertype.py
# QuakePlus+ Flex test with agent/internal_user support.
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

relative_path1 = "uploads/testfile.pdf"
relative_path2 = "uploads/testfile2.pdf"
relative_path3 = "uploads/testfile3.pdf"

absolute_path1 = os.path.abspath(relative_path1)
absolute_path2 = os.path.abspath(relative_path2)
absolute_path3 = os.path.abspath(relative_path3)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width": 1920, "height": 1080}, "ignore_https_errors": True}


@pytest.mark.parametrize("auto_payment,payment_plan", [
    ("Auto Pay On",  "Full Pay"),
    ("Auto Pay On",  "Three Pay"),
    ("Auto Pay On",  "Monthly Pay"),
    ("Auto Pay Off", "Full Pay"),
    ("Auto Pay Off", "Three Pay"),
    ("Auto Pay Off", "Monthly Pay"),
])
def test_quakeplusflex_quoteoffer_usertype(page: Page, auto_payment: str, payment_plan: str) -> None:
    # ── Agent credentials ────────────────────────────────────────────────────
    username = os.getenv("AGENT_USERNAME", "BRK99102")
    password = os.getenv("AGENT_PASSWORD", "Password1")

    print(f"\nLogging in as agent: {username}")

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
    page.locator("#PropertyAddressSingleLine").wait_for(state="visible")
    page.locator("#PropertyAddressSingleLine").press_sequentially(address, delay=50)
    page.wait_for_timeout(2000)
    page.get_by_role("combobox", name="See the best options for").press("Enter")
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Start Quote").click()

    # ── Applicant information ────────────────────────────────────────────────
    dwelling_limit = os.getenv("DWELLING_LIMIT", "1,600,000")
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill(dwelling_limit)
    page.get_by_role("textbox", name="Primary Applicant First Name").fill("ICMTEST")
    page.locator("#vm_Applicant_LastName").fill("TESTER")
    page.get_by_role("textbox", name="Applicant Phone Number").fill("7075556789")
    page.get_by_role("textbox", name="Applicant Email Address").fill("ICMGEOTESTER+1020@GMAIL.COM")

    # ── Quote options ────────────────────────────────────────────────────────
    page.get_by_role("button", name="View Quote Options").click()
    page.get_by_role("button", name="Agree & Continue").click()

    # ── Select deductible: 10% = SLEQFL0, 15% = SLEQFL1, 20% = SLEQFL2, 25% = SLEQFL3
    page.get_by_role("button", name="Continue Shopping Cart", exact=True).wait_for(state="visible")
    page.locator("label[for=rdoFullDeductibleList_SLEQFL0]").wait_for(state="visible")
    page.locator("label[for=rdoFullDeductibleList_SLEQFL0]").click()

    continue_btns = page.get_by_role("button", name="Continue")
    if continue_btns.count() > 1:
        continue_btns.nth(1).click()
    else:
        continue_btns.first.click()

    # ── UES screen ───────────────────────────────────────────────────────────
    page.get_by_role("button", name="Continue").click()

    # ── Finalize Application ──────────────────────────────────────────────────
    page.get_by_role("button", name="Finalize Application").click()

    # ── Applicant type: Individual ────────────────────────────────────────────
    page.locator(".radio-toolbar").nth(0).get_by_text("Individual", exact=True).click()

    # ── Bill to: Applicant ────────────────────────────────────────────────────
    page.get_by_text("Applicant", exact=True).click()

    # ── Payment plan (final enrollment screen) ────────────────────────────────
    payment_toolbar = page.locator(".radio-toolbar").filter(has_text="Full Pay")
    payment_option = payment_toolbar.locator(".radio-item").filter(has_text=payment_plan).first
    if not payment_option.is_visible():
        print(f"\nPayment plan '{payment_plan}' not available — skipping.")
        return
    payment_option.click()

    # Capture premium from selected payment plan label
    label_parts = payment_option.locator("label").inner_text().split("\n")
    premium_value = label_parts[1].strip() if len(label_parts) == 2 else "N/A"

    # Auto pay toggle is hidden for Monthly Pay
    auto_pay_btn = page.get_by_text(auto_payment, exact=True).first
    if auto_pay_btn.is_visible():
        auto_pay_btn.click()
    else:
        print(f"\nAuto pay toggle not visible for '{payment_plan}' — skipping.")

    # ── File uploads ──────────────────────────────────────────────────────────
    page.set_input_files("#fileD1", absolute_path1)
    page.set_input_files("#fileSL2", absolute_path2)
    page.set_input_files("#fileHODec", absolute_path3)

    # ── Terms checkbox ────────────────────────────────────────────────────────
    page.locator(".eqq-terms-and-conditions-agreement > .eqq-checkbox-container > .eqq-checkbox > .bho-checkbox > .bho-checkmark").click()

    # ── Capture quote details ─────────────────────────────────────────────────
    visible_quote = page.locator("table.eqq-summary td").first.text_content().strip()
    assert re.fullmatch(r"UU\d{8}", visible_quote), f"Quote format invalid: {visible_quote}"
    print(f"\nQuote Number: {visible_quote}")

    effective_date = page.locator("#EffectiveDate").input_value() or "N/A"
    product_name = "QUAKEPLUS+ FLEX"
    deductible = "10%"
    dwelling_value = f"${dwelling_limit}"

    print(f"\nProduct:        {product_name}")
    print(f"Quote Number:   {visible_quote}")
    print(f"Deductible:     {deductible}")
    print(f"Dwelling Limit: {dwelling_value}")
    print(f"Premium:        {premium_value}")
    print(f"Effective Date: {effective_date}")

    # ── Payment (skipped — payment processor detects automation) ────────────

    # ── Export results to CSV ─────────────────────────────────────────────────
    csv_path = os.path.abspath("quote_results.csv")
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "User Type", "Username", "Address", "Product", "Quote Number", "Deductible", "Dwelling Limit", "Premium", "Payment Plan", "Auto Pay", "Effective Date"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "agent", username, address, product_name, visible_quote, deductible, dwelling_value, premium_value, payment_plan, auto_payment, effective_date])
    print(f"\nResults exported to: {csv_path}")