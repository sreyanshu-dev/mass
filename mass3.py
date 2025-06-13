from telethon import TelegramClient, functions, types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import asyncio
import os
import random
import time

ACCOUNTS = [{"phone": "+917470479257", "api_id": 29400566, "api_hash": "8fd30dc496aea7c14cf675f59b74ec6f"}]
TARGET_CHANNEL = "The_Grabbers"
REPORT_REASONS = [
    types.InputReportReasonCopyright(),
    types.InputReportReasonSpam(),
    types.InputReportReasonViolence(),
    types.InputReportReasonOther()
]
REPORT_MESSAGES = [
    "Copyright infringement. Remove this channel.",
    "Spam and illegal activities detected.",
    "Violent content found. Immediate action required.",
    "This channel violates Telegram policies.",
    "Repeated copyright violations. Please review."
]
SESSION_DIR = "sessions2"
os.makedirs(SESSION_DIR, exist_ok=True)

def selenium_report(account):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    profile_dir = os.path.join("sessions", "chrome_profiles", account['phone'].replace('+', ''))
    os.makedirs(profile_dir, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={profile_dir}")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("https://web.telegram.org/k/")
        if not os.listdir(profile_dir):
            print(f"[{account['phone']}] Please login manually in the browser window for first time.")
            input(f"After logging in with {account['phone']}, press Enter here to continue...")
        driver.get(f"https://web.telegram.org/k/#{TARGET_CHANNEL}")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "chat-info")))
        menu_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-menu"))
        )
        menu_btn.click()
        time.sleep(1)
        report_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Report')]"))
        )
        report_btn.click()
        time.sleep(1)
        reason = random.choice(["Copyright", "Spam", "Violence", "Other"])
        reason_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{reason}')]"))
        )
        reason_btn.click()
        time.sleep(1)
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        textarea.send_keys(random.choice(REPORT_MESSAGES))
        time.sleep(1)
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Report')]"))
        )
        submit_btn.click()
        print(f"[{account['phone']}] Selenium report sent successfully!")
        time.sleep(random.uniform(2, 5))
        return True
    except Exception as e:
        print(f"[{account['phone']}] Selenium error: {e}")
        return False
    finally:
        driver.quit()

async def telethon_report(account):
    session_file = f"{SESSION_DIR}/{account['phone']}"
    client = TelegramClient(session_file, account['api_id'], account['api_hash'])
    try:
        await client.start()
        if not await client.is_user_authorized():
            print(f"[{account['phone']}] Login required. Skipping Telethon.")
            return False
        channel = await client.get_entity(TARGET_CHANNEL)
        reason = random.choice(REPORT_REASONS)
        message = random.choice(REPORT_MESSAGES)
        for i in range(random.randint(2, 4)):
            result = await client(functions.account.ReportPeerRequest(
                peer=channel,
                reason=reason,
                message=message
            ))
            print(f"[{account['phone']}] Telethon report #{i+1} sent: {result}")
            await asyncio.sleep(random.uniform(2, 6))
        return True
    except Exception as e:
        print(f"[{account['phone']}] Telethon error: {e}")
        return False
    finally:
        await client.disconnect()

async def mass_report():
    cycle = 1
    while True:
        print(f"\n=== Reporting Cycle {cycle} ===")
        for account in ACCOUNTS:
            if random.random() < 0.5:
                await telethon_report(account)
            else:
                selenium_report(account)
            await asyncio.sleep(random.uniform(10, 20))
        print(f"Cycle {cycle} complete. Waiting for next round...\n")
        await asyncio.sleep(random.randint(120, 300))
        cycle += 1

if __name__ == "__main__":
    asyncio.run(mass_report())
      
