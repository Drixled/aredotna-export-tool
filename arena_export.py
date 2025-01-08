from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import argparse
import os
import time

# --- Load Environment Variables ---
load_dotenv()

ARENA_EMAIL = os.getenv("ARENA_EMAIL")
ARENA_PASSWORD = os.getenv("ARENA_PASSWORD")
ARENA_USERNAME = os.getenv("ARENA_USERNAME")
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")

if not ARENA_EMAIL or not ARENA_PASSWORD or not ARENA_USERNAME or not CHROMEDRIVER_PATH:
    raise ValueError("❌ Missing required environment variables. Please check your .env file.")

# --- Parse CLI Arguments ---
parser = argparse.ArgumentParser(description="Are.na Channel Export Script")
parser.add_argument('--all', action='store_true', help='Export all channels')
parser.add_argument('--count', type=int, help='Export a specific number of channels')
parser.add_argument('--name', type=str, help='Export a specific channel by name')

args = parser.parse_args()

# --- Setup WebDriver ---
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

# --- Login to Are.na ---
try:
    driver.get("https://www.are.na/login")
    time.sleep(3)

    # Enter email and password
    driver.find_element(By.ID, "Login--email").send_keys(ARENA_EMAIL)
    driver.find_element(By.ID, "Login--password").send_keys(ARENA_PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]").click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href='/{ARENA_USERNAME}/index']"))
    )
    print("✅ Login successful!")
except Exception as e:
    print(f"❌ Login failed: {e}")
    driver.quit()
    exit()

# --- Fetch Channel Links ---
try:
    driver.get(f"https://www.are.na/{ARENA_USERNAME}/index")
    time.sleep(5)

    # Fetch all channel links
    channels = driver.find_elements(By.CSS_SELECTOR, 'a.c-lfGRGH')
    channel_links = [(channel.get_attribute('href'), channel.text) for channel in channels]

    if not channel_links:
        print("❌ No channels found.")
        driver.quit()
        exit()
except Exception as e:
    print(f"❌ Failed to fetch channels: {e}")
    driver.quit()
    exit()

# --- Export Logic ---
def export_channel(link, index=None):
    try:
        driver.get(link)
        time.sleep(3)

        # Click "More" button
        more_button = driver.find_element(By.XPATH, "//button[contains(@class, 'c-hTwdXI') and contains(text(), 'More')]")
        more_button.click()
        time.sleep(2)

        # Click initial "Download" button
        download_button = driver.find_element(By.XPATH, "//div[@role='menuitem' and contains(@class, 'c-ldqDkB') and contains(text(), 'Download')]")
        download_button.click()
        time.sleep(2)

        # Click confirmation "Download" button
        confirm_download_button = driver.find_element(By.XPATH, "//button[contains(@class, 'c-kiRQBM') and contains(text(), 'Download')]")
        confirm_download_button.click()
        time.sleep(10)

        print(f"✅ Channel exported successfully: {link}")
    except Exception as e:
        print(f"❌ Failed to export channel {index if index else link}: {e}")


# --- Handle Export Options ---
if args.all:
    print("📦 Exporting ALL channels...")
    for index, (link, name) in enumerate(channel_links, start=1):
        print(f"🔗 Exporting Channel {index}: {name} ({link})")
        export_channel(link, index)

elif args.count:
    print(f"📦 Exporting the first {args.count} channels...")
    for index, (link, name) in enumerate(channel_links[:args.count], start=1):
        print(f"🔗 Exporting Channel {index}: {name} ({link})")
        export_channel(link, index)

elif args.name:
    print(f"📦 Searching for channel with name: {args.name}")
    matched_channels = [link for link, name in channel_links if args.name.lower() in name.lower()]
    if matched_channels:
        for index, link in enumerate(matched_channels, start=1):
            print(f"🔗 Exporting Matched Channel {index}: {link}")
            export_channel(link, index)
    else:
        print(f"❌ No channel found with the name: {args.name}")

else:
    print("📦 No specific option provided. Exporting the first 5 channels by default...")
    for index, (link, name) in enumerate(channel_links[:5], start=1):
        print(f"🔗 Exporting Channel {index}: {name} ({link})")
        export_channel(link, index)

# --- Cleanup ---
driver.quit()
print("🎯 Script completed successfully!")
