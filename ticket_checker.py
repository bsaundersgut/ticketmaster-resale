import sys
import os
import time
import winsound
import io
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
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress warnings

# Auto-allow notifications and location
prefs = {
    "profile.default_content_setting_values.notifications": 1,
    "profile.default_content_setting_values.geolocation": 1
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# ─── Ticketmaster Event Page ───
url = "https://www.ticketmaster.ie/all-together-now-weekend-camping-portlaw-31-07-2025/event/18006117864E1B03"
driver.get(url)

def check_for_resale():
    """Check if resale tickets are available."""
    try:
        # If placeholder is missing, maybe resale section changed
        placeholder = driver.find_elements(By.XPATH, '//*[contains(text(), "Resale Tickets will appear below when they are available.")]')

        if not placeholder:
            print("📛 Placeholder missing — possibly updating/resale incoming...")
            return False

        buttons = driver.find_elements(By.XPATH, '//button[contains(., "Weekend Camping")]')

        if buttons:
            print(f"🎯 Resale ticket(s) found: {[btn.text for btn in buttons]}")
            winsound.Beep(1000, 1000)
            print("🛑 Manual intervention mode — browser paused for purchase.")
            return True
        else:
            print("❌ No 'Weekend Camping' resale tickets found.")
            return False
    except Exception as e:
        print(f"❌ Error checking resale: {e}")
        return False

def wait_for_dom_update(wait_seconds=5):
    """Wait for DOM to update by monitoring a known element (resale section) disappearing then reappearing."""
    try:
        print("⏳ Waiting for page to update...")
        WebDriverWait(driver, wait_seconds).until_not(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Resale Tickets will appear below when they are available.")]'))
        )
        WebDriverWait(driver, wait_seconds).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ticketSelection")]'))
        )
        print("✅ Page updated.")
    except:
        print("⚠️ Timeout or element not changed — continuing anyway.")

# ─── Main Smart Loop ───
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

        # Smart wait for DOM update after clicking "Find Tickets"
        wait_for_dom_update(wait_seconds=6)

        #Inject fake resale ticket (for test only)
        # driver.execute_script("""
            # let btn = document.createElement("button");
            # btn.innerText = "Weekend Camping - Resale €199";
            # btn.style.margin = "10px";
            # btn.style.padding = "10px";
            # btn.style.background = "#d00";
            # btn.style.color = "#fff";
            # btn.className = "tm-button";
            # document.body.appendChild(btn);
        # """)

        found = check_for_resale()
        if found:
            break


        found = check_for_resale()
        if found:
            break

        # Click "Search Again" if needed
        try:
            search_again = WebDriverWait(driver, 6).until(
                EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Search Again"]]'))
            )
            print("🔁 Clicking 'Search Again' to retry...")
            search_again.click()
        except Exception as e:
            print(f"🔄 'Search Again' not found or failed: {e}")

        # Wait for "Search Again" to take effect
        wait_for_dom_update(wait_seconds=5)

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
