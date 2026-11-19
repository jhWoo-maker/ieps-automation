import asyncio
from playwright.async_api import async_playwright

async def check_popover_open():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.goto("http://localhost:8501")
        await page.wait_for_timeout(3000)
        
        # Click the IEPS 폴더 button
        button = page.locator('button[data-testid="stPopoverButton"]')
        await button.click()
        await page.wait_for_timeout(1000)
        
        # Check text inside popover
        popover_text = await page.locator('[data-testid="stPopoverBody"]').inner_text() if await page.locator('[data-testid="stPopoverBody"]').count() > 0 else "Not found"
        print("Popover body text:", popover_text)
        
        await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\check_top_right_popover_opened.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_popover_open())
