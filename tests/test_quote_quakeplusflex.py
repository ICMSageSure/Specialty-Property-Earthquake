import re
from playwright.sync_api import Page, expect
import os
import pytest
import random
import Login from '../pages/MGS_LOGIN.py'
import StartNewQuote from '../pages/MGS_STARTNEWQUOTE.py'

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {"viewport": {"width":1920,"height":1080}}


