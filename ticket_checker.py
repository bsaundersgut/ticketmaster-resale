import sys
import os
import time
import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ─── Suppress Native Chromium Logs ───
sys.stderr = open(os.devnull, 'w')

# ─── Setup WebDriver ───
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Auto-allow notifications and location
prefs = {
    "profile.default_content_setting_values.notifications": 1,
    "profile.default_content_setting_values.geolocation": 1
}
options.add_experimental_option("prefs", prefs)

# ─── Launch WebDriver ───
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ─── Ticketmaster Event URL ───
url = "https://www.ticketmaster.ie/all-together-now-weekend-camping-portlaw-31-07-2025/event/18006117864E1B03"
driver.get(url)

# Accept Cookies if Prompt Appears
try:
    accept_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept Cookies"]'))
    )
    accept_btn.click()
    print("🍪 Accepted cookies.")
except:
    print("🍪 No cookie prompt found.")

def wait_for_resale_span(timeout=5):
    """Wait for the 'Verified Resale Ticket' span to appear."""
    try:
        print(f"⏳ Waiting up to {timeout}s for Verified Resale Ticket to appear...")
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(), "Verified Resale Ticket")]')
            )
        )
        print("✅ Verified Resale Ticket span found.")
        return True
    except:
        print("❌ No Verified Resale Ticket span found after timeout.")
        return False

def check_for_resale():
    """Check if resale ticket span is present."""
    try:
        spans = driver.find_elements(By.XPATH, '//span[contains(text(), "Verified Resale Ticket")]')
        if spans:
            print(f"🎯 Resale ticket(s) found! Count: {len(spans)}")
            winsound.Beep(1000, 1500)
            print("🛑 Manual intervention mode — browser paused for purchase.")
            return True
        else:
            print("❌ No resale tickets found.")
            return False
    except Exception as e:
        print(f"❌ Error during resale check: {e}")
        return False

# ─── Main Loop ───
try:
    while True:
        try:
            find_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="findTicketsBtn"]'))
            )
            print("🔍 Clicking 'Find Tickets'...")
            find_btn.click()
        except Exception as e:
            print(f"⚠️ Couldn't click 'Find Tickets': {e}")
            break

        wait_for_resale_span(timeout=5)
        found = check_for_resale()
        if found:
            break

        try:
            search_again = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Search Again"]]'))
            )
            print("🔁 Clicking 'Search Again' to retry...")
            search_again.click()
        except Exception as e:
            print(f"🔄 'Search Again' not found or failed: {e}")

except KeyboardInterrupt:
    print("🛑 Script interrupted manually.")
finally:
    print("🔚 Script finished or awaiting manual action. Press Ctrl+C to close.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("👋 Exiting by user request.")
        driver.quit()
