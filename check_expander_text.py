from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:8501')
    page.wait_for_timeout(3000)
    page.locator('[data-testid="stRadioOption"]').filter(has_text="4. 배출시설 운영현황").click()
    page.wait_for_timeout(2000)
    
    summary_text = page.locator('details summary').first.inner_text()
    print('Summary inner text:', repr(summary_text))
    
    browser.close()
