class StartNewQuote:
    def __init__(self, page):
        self.page = page

    def start_quote(self):
        self.page.click("text=Start New Quote")
        self.page.wait_for_navigation()

    def modal_start_eq_quote(self):
        self.page.click("text=Residential Earthquake Products")
        self.page.click("button:has-text('OK')")

    def modal_start_homeowners_quote(self):
        self.page.click("text=GeoVera Specialty Insurance Company - surplus lines")
        self.page.click("button:has-text('OK')")
        

    