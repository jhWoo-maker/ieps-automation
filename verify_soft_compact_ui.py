import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:8501")
        await page.wait_for_timeout(3000)

        # Screenshot of main page with compact soft font
        await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\compact_soft_font_mod1.png", full_page=False)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
