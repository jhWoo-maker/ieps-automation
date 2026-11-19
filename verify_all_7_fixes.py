import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 950})
        await page.goto("http://localhost:8501")
        await page.wait_for_timeout(3000)

        # Module 1
        await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\fix_mod1.png", full_page=False)

        # Select Module 5 (배출구 가동시간)
        mod5_radio = page.locator("label:has-text('5. 배출구 가동시간')")
        if await mod5_radio.count() > 0:
            await mod5_radio.click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\fix_mod5.png", full_page=False)

        # Select Module 8 (연료사용량)
        mod8_radio = page.locator("label:has-text('8. 연료사용량')")
        if await mod8_radio.count() > 0:
            await mod8_radio.click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\fix_mod8.png", full_page=False)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
