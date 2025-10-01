import os
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    base_path = "file://" + os.getcwd()

    # Verify demo-it-business.html
    page.goto(f"{base_path}/demo-it-business.html")
    page.wait_for_selector('h1', state='visible')
    page.wait_for_timeout(500) # wait for animations to settle
    page.screenshot(path="jules-scratch/verification/screenshot-home.png")

    # Verify demo-it-business-about.html
    page.goto(f"{base_path}/demo-it-business-about.html")
    page.wait_for_selector('h1', state='visible')
    page.wait_for_timeout(500)
    page.screenshot(path="jules-scratch/verification/screenshot-about.png")

    # Verify temoignages.html
    page.goto(f"{base_path}/temoignages.html")
    page.wait_for_selector('h1', state='visible')
    page.wait_for_timeout(500)
    page.screenshot(path="jules-scratch/verification/screenshot-testimonials.png")

    # Verify faq.html
    page.goto(f"{base_path}/faq.html")
    page.wait_for_selector('h1', state='visible')
    page.wait_for_timeout(500)
    page.screenshot(path="jules-scratch/verification/screenshot-faq.png")

    # Verify methodologie.html
    page.goto(f"{base_path}/methodologie.html")
    page.wait_for_selector('h1', state='visible')
    page.wait_for_timeout(500)
    page.screenshot(path="jules-scratch/verification/screenshot-methodology.png")

    # Verify demo-it-business-case-studies.html
    page.goto(f"{base_path}/demo-it-business-case-studies.html")
    page.wait_for_selector('h1', state='visible')
    page.wait_for_timeout(500)
    page.screenshot(path="jules-scratch/verification/screenshot-case-studies.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)