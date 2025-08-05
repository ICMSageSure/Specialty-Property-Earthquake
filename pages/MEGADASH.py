class StartNewQuote:
    def __init__(self, page):
        self.page = page

    def start_quote(self):
        self.page.click("text=Start New Quote")
        self.page.wait_for_load_state("networkidle")