import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get absolute path for the files
        base_path = os.path.abspath('.')

        # Verify demo-it-business.html
        await page.goto(f"file://{os.path.join(base_path, 'demo-it-business.html')}")
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(2000) # Wait for animations
        await page.screenshot(path="jules-scratch/verification/screenshot-home.png", full_page=True)

        # Verify demo-it-business-about.html
        await page.goto(f"file://{os.path.join(base_path, 'demo-it-business-about.html')}")
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(2000) # Wait for animations
        await page.screenshot(path="jules-scratch/verification/screenshot-about.png", full_page=True)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())