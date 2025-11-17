# this test case will generate a quote for QuakePlusFlex 10% deductible with Full Pay and Auto Pay On

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

test_credit_card_numbers = ["4111111111111111",
                            "5431111111111111",
                            "341111111111111",


]



def test_quote_quakeplusflex_5percent(page: Page) -> None:
    applicant_type = os.getenv("APPLICANT_TYPE", "LLC")

    # Payment Plan: Full Pay, Three Pay, Monthly Pay
    payment_plan = os.getenv("PAYMENT_PLAN", "Three Pay$")

    # Auto Payment: Auto Pay On, Auto Pay Off
    auto_payment = os.getenv("AUTO_PAYMENT", "Auto Pay On")

    # QuakePlus+ Flex Deductible Percent options: 10%, 15%, 20%, 25%
    # deductible_percent = os.getenv("DEDUCTIBLE_PERCENT", "10%")

    # Applicant Choice: Applicant, Alternate Payor, Mortgagee
    bill_to = os.getenv("BILL_TO", "Alternate Payor")

    page.goto("https://tst.mygeosource.com/")
    page.get_by_role("textbox", name="Policyholder Email or Agent").fill("BRK99102")
    page.get_by_role("textbox", name="Password").fill("Password1")
    screenshot_path1 = "screenshot_login.png"
    page.screenshot(path=screenshot_path1, full_page=True)

    page.get_by_role("button", name="Log In", exact=True).click()
    page.get_by_role("paragraph").filter(has_text="Start New Quote").get_by_role("link").click()
    page.locator("[id=\"optionResidential\\ Earthquake\"]").get_by_text("Residential Earthquake Products").click()
    screenshot_path2 = "screenshot_newquote.png"
    page.screenshot(path=screenshot_path2, full_page=True)
    page.get_by_role("button", name="OK").click()

    page.locator("#PropertyAddressSingleLine").wait_for(state="visible")
    page.locator("#PropertyAddressSingleLine").click()
    page.locator("#PropertyAddressSingleLine").fill("36 PELICAN CREST DR, NEWPORT COAST, CA 92657-1805")
    page.wait_for_timeout(1000)
    # page.locator("#PropertyAddressSingleLine").press("ArrowDown")
    screenshot_path3 = "screenshot_address.png"
    page.screenshot(path=screenshot_path3, full_page=True)
    page.wait_for_timeout(1000)

    page.get_by_role("combobox", name="See the best options for").press("Enter")
    page.get_by_role("button", name="Start Quote").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").click()
    page.get_by_role("textbox", name="Current Companion Insurance Policy Coverage A Dwelling Limit").fill("4,600,000")
    page.get_by_role("textbox", name="Primary Applicant First Name").click()
    page.get_by_role("textbox", name="Primary Applicant First Name").press("CapsLock")
    page.get_by_role("textbox", name="Primary Applicant First Name").fill("ICMTEST")
    page.locator("#vm_Applicant_LastName").click()
    page.locator("#vm_Applicant_LastName").fill("TESTER")
    page.get_by_role("textbox", name="Applicant Phone Number").click()
    page.get_by_role("textbox", name="Applicant Phone Number").fill("7075551234")
    page.get_by_role("textbox", name="Applicant Email Address").click()
    page.get_by_role("textbox", name="Applicant Email Address").fill("ICMGEOTESTER@GMAIL.COM")
    screenshot_path4 = "screenshot_applicant_info.png"
    page.screenshot(path=screenshot_path4, full_page=True)

    page.get_by_role("button", name="View Quote Options").click()
    page.get_by_role("button", name="Agree & Continue").click()
    # page.locator("#lnkExpandAll").click()
    page.get_by_role("button", name="Continue Shopping Cart", exact=True).wait_for(state="visible")
    continue_btns = page.get_by_role("button", name="Continue")
    page.locator("label[for=rdoFullDeductibleList_SLEQFL0]").wait_for(state="visible")
    # QuakePlus+ Flex Deductible Percent options: SLEQFL0 = 10%, 
    #                                             SLEQFL1 = 15%, 
    #                                             SLEQFL2 = 20%, 
    #                                             SLEQFL3 = 25%

    page.locator("label[for=rdoFullDeductibleList_SLEQFL0]").click()
    
    screenshot_path5 = "screenshot_quote_options.png"
    page.screenshot(path=screenshot_path5, full_page=True)
    if continue_btns.count() > 1:
    # If more than one, click the second button
        continue_btns.nth(1).click()
    else:
    # Otherwise, click the only button
        continue_btns.first.click()

    screenshot_path6 = "screenshot_ues.png"
    page.screenshot(path=screenshot_path6, full_page=True)
    page.get_by_role("button", name="Continue").click()

    screenshot_path7 = "screenshot_finalize_application.png"
    page.screenshot(path=screenshot_path7, full_page=True)
    page.get_by_role("button", name="Finalize Application").click()


    
    toolbars = page.locator(".radio-toolbar")

    # 1st toolbar = applicant type
    toolbars.nth(0).get_by_text(applicant_type, exact=True).click()
    print(f"\nSelected Applicant Type: \n{applicant_type}")
    if applicant_type == "Individual":
        page.get_by_text("Applicant", exact=True).click()
        # Fill in applicant information
        # page.locator("#Applicant_FirstName").fill("ICMTEST")
        # page.locator("#Applicant_LastName").fill("TESTER")
        # page.locator("#Applicant_PhoneNumber").fill("7075551234")
        # page.locator("#ApplicantEmailAddress").fill("ICMGEOTESTER@GMAIL.COM")
    elif applicant_type == "LLC":
        page.get_by_text("LLC", exact=True).click()
        # Fill in the alternate payor information
        page.locator("#Entity").fill("ICMTEST ENTITYLLC")
        page.locator("#ManagingMember_FirstName").fill("LLC ICMFIRSTNAME")
        page.locator("#ManagingMember_LastName").fill("ICMLASTNAME")
    elif applicant_type == "Trust":
        page.get_by_text("Trust", exact=True).click()
        # Fill in mortgagee information
        page.locator("#Entity").fill("ICMTEST ENTITYLLC")
        page.locator("#ManagingMember_FirstName").fill("LLC ICMFIRSTNAME")
        page.locator("#ManagingMember_LastName").fill("ICMLASTNAME")
    elif applicant_type == 'Estate':
        page.get_by_text("Estate", exact=True).click()
        # Fill in estate information
        page.locator("#Entity").fill("ICMTEST ENTITYESTATE")
        page.locator("#ManagingMember_FirstName").fill("ESTATE ICMFIRSTNAME")
        page.locator("#ManagingMember_LastName").fill("ICMLASTNAME")
    elif applicant_type == 'Corporation':
        page.get_by_text("Corporation", exact=True).click()
        # Fill in corporation information
        page.locator("#Entity").fill("ICMTEST ENTITYCORPORATION")
        page.locator("#ManagingMember_FirstName").fill("CORPORATION ICMFIRSTNAME")
        page.locator("#ManagingMember_LastName").fill("ICMLASTNAME")
    else:
        raise ValueError(f"Unknown bill to choice: {bill_to_choice}")



    page.locator(".radio-toolbar")
# Set this variable to one of: 'Applicant', 'Alternate Payor', 'Mortgagee'
    bill_to_choice = bill_to
    print(f"\n\nSelected Bill To Choice: \n{bill_to_choice}\n")
    if bill_to_choice == "Applicant":
        page.get_by_text("Applicant", exact=True).click()
        # Fill in applicant information
        # page.locator("#Applicant_FirstName").fill("ICMTEST")
        # page.locator("#Applicant_LastName").fill("TESTER")
        # page.locator("#Applicant_PhoneNumber").fill("7075551234")
        # page.locator("#ApplicantEmailAddress").fill("ICMGEOTESTER@GMAIL.COM")
    elif bill_to_choice == "Alternate Payor":
        page.get_by_text("Alternate Payor", exact=True).click()
        # Fill in the alternate payor information
        page.locator("#AlternatePayor_Addressee1").fill("ICMTEST ALTPAYOR")
        page.locator("#AlternatePayor_Street").fill("1455 ALTERNATE RD")
        page.locator("#AlternatePayor_City").fill("FAIRFIELD")
        page.locator("#AlternatePayor_State").select_option("CA")
        page.locator("#AlternatePayor_ZipCode").fill("94534")
        page.locator("#AlternatePayorLoanNumber").fill("11223344")
    elif bill_to_choice == "Mortgagee":
        page.get_by_text("Mortgagee", exact=True).click()
        # Fill in mortgagee information
        page.locator('#btn-edit-mortgagee').click()
        page.locator("#Mortgagee1_Addressee1").fill("ICMTEST MORTGAGEE")
        page.locator("#Mortgagee1_Addressee2").fill("")
        page.locator("#Mortgagee1LoanNumber").fill("11223344")
        page.locator("#Mortgagee1_Street").fill("1455 MORTGAGEE RD")
        page.locator("#Mortgagee1_City").fill("FAIRFIELD")
        page.locator("#Mortgagee1_State").select_option("CA")
        page.locator("#Mortgagee1_ZipCode").fill("94534")
    else:
        raise ValueError(f"Unknown bill to choice: {bill_to_choice}")

    payment_type = page.get_by_text(payment_plan)
    payment_type.click()
    print(f"Selected Payment Type: \n{payment_type.inner_text()}\n")
    auto_pay_onoff = page.get_by_text(auto_payment, exact=True)
    auto_pay_onoff.click()
    print(f"Selected Auto Pay: \n{auto_pay_onoff.inner_text()}\n")
    page.set_input_files("#fileD1",
                    absolute_path1)
    page.set_input_files("#fileSL2",
                absolute_path2)
    page.set_input_files("#fileHODec",
                absolute_path3)
    page.locator(".eqq-terms-and-conditions-agreement > .eqq-checkbox-container > .eqq-checkbox > .bho-checkbox > .bho-checkmark").click()
    td_text = page.locator('table.eqq-summary td').first.text_content()
    match = re.fullmatch(r"UU\d{8}", td_text.strip())
    print(f"Quote Number:\n{td_text.strip()}\n")
    payment_toolbar = page.locator('.radio-toolbar').filter(has_text="Full Pay")
    radio_items = payment_toolbar.locator('.radio-item')
    for i in range(radio_items.count()):
        label_text = radio_items.nth(i).locator('label').inner_text().split('\n')
        if len(label_text) == 2:
            plan, amount = label_text
            if plan.strip() in ["Full Pay", "Three Pay", "Monthly Pay"]:
                print(f"{plan.strip()}: \n{amount.strip()}")
        else:
            print(f"Unknown format: {label_text}")
    screenshot_path8 = "screenshot_quotation_enrollment.png"
    page.screenshot(path=screenshot_path8, full_page=True)
    page.get_by_role("button", name="Pay Now").click()
    # page.get_by_text("Mail Form Later").click()
    page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("link", name="Add new payment method").wait_for(state="visible")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("link", name="Add new payment method").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter card number").wait_for(state="visible")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter card number").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter card number").press_sequentially(random.choice(test_credit_card_numbers), delay=100)
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Expiration Date").press("Tab")  
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Expiration Date").click()  
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Expiration Date").press_sequentially("11/26")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter name as it").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter name as it").press("Tab")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("textbox", name="Please, enter name as it").press_sequentially("ICMTEST TESTER")
    # page.get_by_role("dialog", name="Payment method").content_frame.locator("#billingAddress").press("Tab")
    # page.get_by_role("dialog", name="Payment method").content_frame.locator("#billingAddress").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.locator("#billingAddress").press_sequentially("1455 OLIVER RD")
    # page.get_by_role("dialog", name="Payment method").content_frame.locator("#billingZip").press("Tab")
    # page.get_by_role("dialog", name="Payment method").content_frame.locator("#billingZip").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.locator("#billingZip").press_sequentially("94534")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Save").wait_for(state="visible")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Submit").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Next").wait_for(state="visible")    
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Next").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Enroll").wait_for(state="visible")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Enroll").click()
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Close").wait_for(state="visible")
    # page.get_by_role("dialog", name="Payment method").content_frame.get_by_role("button", name="Close").click()
