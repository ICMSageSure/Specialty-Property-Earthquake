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