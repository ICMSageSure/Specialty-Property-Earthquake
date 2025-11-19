from actions import LoginActions
from pages.dashboard_page import DashboardPage


def test_user_can_login(login_actions: LoginActions, page) -> None:
    login_actions.login()
    dashboard = DashboardPage(page)
    dashboard.wait_for_ready()
