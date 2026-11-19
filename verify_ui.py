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
        
        # Take initial screenshot
        artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34"
        screen_path1 = os.path.join(artifact_dir, "ui_verification_1.png")
        await page.screenshot(path=screen_path1, full_page=True)
        print(f"Initial screenshot saved to {screen_path1}")
        
        # Select module 6 from sidebar radio buttons
        labels = page.locator("div[data-testid='stSidebar'] label")
        count = await labels.count()
        print(f"Sidebar radio count: {count}")
        for i in range(count):
            txt = await labels.nth(i).text_content()
            if "6. 대기 방지시설" in txt:
                print(f"Clicking module 6 label: {txt}")
                await labels.nth(i).click()
                await page.wait_for_timeout(2000)
                break
                
        # Upload 6.대기_방지시설_운영현황(26년_10월) (1).xlsm into Module 6
        file_input = page.locator("input[type='file']").first
        xlsm_path = r"c:\Users\user\Downloads\6.대기_방지시설_운영현황(26년_10월) (1).xlsm"
        if os.path.exists(xlsm_path) and await file_input.count() > 0:
            print(f"Uploading XLSM file: {xlsm_path}")
            await file_input.set_input_files(xlsm_path)
            await page.wait_for_timeout(3000)
            
        # Click sidebar validation button
        btn = page.locator("button:has-text('데이터 검증하기')")
        if await btn.count() > 0:
            print("Clicking '🔍 데이터 검증하기' button in sidebar...")
            await btn.click()
            await page.wait_for_timeout(3000)
            
        screen_path2 = os.path.join(artifact_dir, "ui_verification_2.png")
        await page.screenshot(path=screen_path2, full_page=True)
        print(f"Final screenshot saved to {screen_path2}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
