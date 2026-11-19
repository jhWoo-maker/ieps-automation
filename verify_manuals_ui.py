import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        
        print("Navigating to http://localhost:8501...")
        await page.goto("http://localhost:8501", timeout=15000)
        await page.wait_for_timeout(3000)
        
        artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34"
        
        # Module 1 screenshot
        screen_path1 = os.path.join(artifact_dir, "manual_verification_mod1.png")
        await page.screenshot(path=screen_path1, full_page=False)
        print(f"Module 1 screenshot saved to {screen_path1}")
        
        # Select module 6 from sidebar
        labels = page.locator("div[data-testid='stSidebar'] label")
        count = await labels.count()
        for i in range(count):
            txt = await labels.nth(i).text_content()
            if "6. 대기 방지시설" in txt:
                await labels.nth(i).click()
                await page.wait_for_timeout(2000)
                break
                
        screen_path6 = os.path.join(artifact_dir, "manual_verification_mod6.png")
        await page.screenshot(path=screen_path6, full_page=False)
        print(f"Module 6 screenshot saved to {screen_path6}")

        # Select module 9 from sidebar
        for i in range(count):
            txt = await labels.nth(i).text_content()
            if "9. 기타화학물질" in txt:
                await labels.nth(i).click()
                await page.wait_for_timeout(2000)
                break

        screen_path9 = os.path.join(artifact_dir, "manual_verification_mod9.png")
        await page.screenshot(path=screen_path9, full_page=False)
        print(f"Module 9 screenshot saved to {screen_path9}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
