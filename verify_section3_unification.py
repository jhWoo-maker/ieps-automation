import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto('http://localhost:8501')
    page.wait_for_timeout(3000)

    # Check Module 6
    page.locator('[data-testid="stRadioOption"]').filter(has_text='6. 대기 방지시설 운영현황').click()
    page.wait_for_timeout(2000)
    img_path = os.path.join(artifact_dir, "unified_section3_mod6.png")
    page.screenshot(path=img_path)
    print(f"Saved {img_path}")

    # Check Module 1
    page.locator('[data-testid="stRadioOption"]').filter(has_text='1. 대기-자가측정기록부').click()
    page.wait_for_timeout(2000)
    img_path1 = os.path.join(artifact_dir, "unified_section3_mod1.png")
    page.screenshot(path=img_path1)
    print(f"Saved {img_path1}")

    browser.close()

print("Verification completed successfully.")
