import pytest
import re
import os
from playwright.sync_api import Page, expect
import pdfplumber

relative_path = "uploads/testfile.pdf"

absolute_path = os.path.abspath(relative_path)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width":1920,"height":1080}}


def test_example(page: Page) -> None:
    page.goto("https://tst.mygeosource.com/")
    page.get_by_role("textbox", name="Policyholder Email or Agent").click()
    page.get_by_role("textbox", name="Policyholder Email or Agent").fill("BRK99102")
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Password").fill("Password1")
    page.get_by_role("button", name="Log In", exact=True).click()
    page.wait_for_selector("text=Hello,")
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
    if page.get_by_role("textbox", name="Year Built").is_visible():
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
    page.get_by_role("textbox", name="Applicant Email Address").fill("ICMGEOTESTER+1020@GMAIL.COM")
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
    page.get_by_role("button", name="Print/Download Quotes").click()
    page.locator("label:nth-child(5) > .checkmark").first.click()
    # The Print Quote action may open a popup that navigates to a PDF (not a download event).
    # Capture the popup and save the PDF bytes to a temp file for pdfplumber to open.
    with page.expect_popup() as popup_info:
        page.get_by_role("button", name="Print Quote Offer").click()
    popup = popup_info.value
    popup.wait_for_load_state()
    # Try to find a response with a PDF content-type
    try:
        response = popup.wait_for_response(lambda r: 'application/pdf' in (r.headers.get('content-type') or ''), timeout=5000)
        pdf_bytes = response.body()
    except Exception:
        # fallback: try to fetch the popup URL. Handle blob/data/about URLs by evaluating
        # inside the popup and returning a base64 string of the PDF bytes.
        from base64 import b64decode
        url = popup.url
        if url.startswith("blob:") or url.startswith("data:") or url.startswith("about:"):
            # Evaluate in the popup to fetch the PDF and return base64-encoded string
            base64_pdf = popup.evaluate(
                "async () => {\n"
                "  const res = await fetch(location.href);\n"
                "  const buf = await res.arrayBuffer();\n"
                "  let binary = '';\n"
                "  const bytes = new Uint8Array(buf);\n"
                "  for (let i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);\n"
                "  return btoa(binary);\n"
                "}"
            )
            pdf_bytes = b64decode(base64_pdf)
        else:
            resp = page.context.request.get(url)
            pdf_bytes = resp.body()

    import tempfile
    tmpf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    tmpf.write(pdf_bytes)
    tmpf.close()
    pdf_path = tmpf.name
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        assert "ICMTEST TESTER" in text, "Applicant name not found in PDF"
        assert "Dwelling Limit: $600,000" in text, "Dwelling Limit not found in PDF"
        assert re.search(r"Quote Number:\s*QP\d{8}", text), "Quote Number format invalid in PDF"
        print("\nPDF content verified successfully.")

    # page.pause()