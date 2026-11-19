import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:8501")
        await page.wait_for_timeout(3000)

        # Module 1
        await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\layout_mod1.png", full_page=False)

        # Select Module 6
        mod6_radio = page.locator("label:has-text('6. 대기 방지시설 운영현황')")
        if await mod6_radio.count() > 0:
            await mod6_radio.click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\layout_mod6.png", full_page=False)

        # Select Module 10
        mod10_radio = page.locator("label:has-text('10. 원부원료 사용량 및 제품 생산량')")
        if await mod10_radio.count() > 0:
            await mod10_radio.click()
            await page.wait_for_timeout(2000)
            await page.screenshot(path=r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34\layout_mod10.png", full_page=False)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
