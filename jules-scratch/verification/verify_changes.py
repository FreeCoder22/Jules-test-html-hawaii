import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Get the absolute path for the files
        base_path = os.path.abspath('.')

        # Pages to verify
        pages_to_verify = [
            "demo-it-business.html",
            "demo-it-business-about.html",
            "demo-it-business-services-details-ia.html",
            "demo-it-business-services-details-power-platform.html",
            "demo-it-business-services-details-dev-azure.html",
            "demo-it-business-services-details-migrate.html",
            "demo-it-business-services-details-ux.html",
            "demo-it-business-services-details-agile.html",
            "demo-it-business-services-details-run.html"
        ]

        for file in pages_to_verify:
            file_path = f"file://{os.path.join(base_path, file)}"
            screenshot_path = f"jules-scratch/verification/{file.replace('.html', '.png')}"

            print(f"Navigating to {file_path}")
            await page.goto(file_path)

            # Wait for the page to be fully loaded, especially if there are animations
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2) # Additional wait for animations

            print(f"Taking screenshot of {file}")
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())