import os
from playwright.sync_api import sync_playwright

def run_verification():
    """
    Navigates to the final modified HTML files and takes screenshots to verify the changes.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # --- Verify demo-it-business.html ---
        home_page_path = os.path.abspath('demo-it-business.html')
        print(f"Navigating to file://{home_page_path}")
        page.goto(f"file://{home_page_path}")
        page.wait_for_load_state('networkidle')
        page.screenshot(path="jules-scratch/verification/final_homepage.png", full_page=True)
        print("  - Captured screenshot of the final homepage.")

        # --- Verify demo-it-business-about.html ---
        about_page_path = os.path.abspath('demo-it-business-about.html')
        print(f"Navigating to file://{about_page_path}")
        page.goto(f"file://{about_page_path}")
        page.wait_for_load_state('networkidle')
        page.screenshot(path="jules-scratch/verification/final_aboutpage.png", full_page=True)
        print("  - Captured screenshot of the final about page.")

        browser.close()

if __name__ == '__main__':
    run_verification()