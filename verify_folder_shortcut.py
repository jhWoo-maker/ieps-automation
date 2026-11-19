import os
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\ad521db9-e8bb-4b72-8409-212c96a01c34"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto('http://localhost:8501')
    page.wait_for_timeout(3000)

    # Screenshot Module 1 with Folder Shortcut
    img_path = os.path.join(artifact_dir, "folder_shortcut_top_mod1.png")
    page.screenshot(path=img_path)
    print(f"Saved {img_path}")

    browser.close()

print("Captured folder shortcut screenshot.")
