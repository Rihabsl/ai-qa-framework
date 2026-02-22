import os
import pytest
from playwright.sync_api import sync_playwright
from core.ai_engine.self_healer import SelfHealer
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope='session')
def browser_ctx():
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            record_video_dir='reports/videos/'
        )
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(browser_ctx):
    p = browser_ctx.new_page()
    yield p
    p.close()

@pytest.fixture(scope='session')
def healer():
    return SelfHealer()