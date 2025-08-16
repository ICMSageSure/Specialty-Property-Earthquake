import os
from dotenv import load_dotenv

class Login:
    def __init__(self, page):
        self.page = page
        load_dotenv()
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.url = os.getenv("BASE_URL")

    def navigate_to_login(self):
        self.page.goto(self.url)

    def login(self):
        self.enter_username = self.page.fill('#txtUserId', self.username)
        self.enter_password = self.page.fill('#txtPassword', self.password)
        self.page.click('#btnLogin')
        self.page.wait_for_navigation()

    def create_an_account(self):
        self.page.click('#btnCreateAccount')
        self.page.wait_for_navigation()

    def guest_login(self):
        self.page.click('#btnGuest')
        self.page.wait_for_navigation()

    def coastal_select_insurance_link(self):
        self.page.click('#csLink')

    def geovera_insurance_link(self):
        self.page.click('#gvLink')

    def gvsic_link(self):
        self.page.click('#gvsLink')
    
    def gvais_link(self):
        self.page.click('#gvaisLink')