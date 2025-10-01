import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    base_path = os.path.abspath('.')

    # 1. Verify the homepage
    homepage_path = os.path.join(base_path, 'demo-it-business.html')
    page.goto(f'file://{homepage_path}')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='jules-scratch/verification/homepage.png')
    print("Screenshot taken for homepage.")

    # 2. Verify the about page
    about_page_path = os.path.join(base_path, 'demo-it-business-about.html')
    page.goto(f'file://{about_page_path}')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='jules-scratch/verification/about-page.png')
    print("Screenshot taken for about page.")

    # 3. Verify a services detail page
    services_page_path = os.path.join(base_path, 'demo-it-business-services-details-dev-azure.html')
    page.goto(f'file://{services_page_path}')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='jules-scratch/verification/services-detail-page.png')
    print("Screenshot taken for services detail page.")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)