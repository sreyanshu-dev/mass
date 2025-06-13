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

ACCOUNTS = [
    {"phone": "+917470479257", "api_id": 29400566, "api_hash": "8fd30dc496aea7c14cf675f59b74ec6f"},
    {"phone": "+919343771145", "api_id": 29400566, "api_hash": "8fd30dc496aea7c14cf675f59b74ec6f"},
    #{"phone": "+917470479257", "api_id": 29400566, "api_hash": "8fd30dc496aea7c14cf675f59b74ec6f"}
]
TARGET_CHANNEL = "The_Grabbers"
REPORT_REASONS = [
    types.InputReportReasonCopyright(),
    types.InputReportReasonSpam(),
    types.InputReportReasonViolence(),
    types.InputReportReasonOther()
]
REPORT_MESSAGES = [
    "Copyright infringement. Remove this channel.",
    "Spam activities detected.",
    "Violent content found. Immediate action required.",
    "This channel violates Telegram policies.",
    "Repeated copyright violations. Please review."
]
SESSION_DIR = "sessions2"
os.makedirs(SESSION_DIR, exist_ok=True)

async def telethon_report(account):
    session_file = f"{SESSION_DIR}/{account['phone']}"
    client = TelegramClient(session_file, account['api_id'], account['api_hash'])
    try:
        await client.start()
        if not await client.is_user_authorized():
            print(f"[{account['phone']}] Login required. Skipping Telethon.")
            return False
        channel = await client.get_entity(TARGET_CHANNEL)
        for i in range(50):
            reason = random.choice(REPORT_REASONS)
            message = random.choice(REPORT_MESSAGES)
            result = await client(functions.account.ReportPeerRequest(
                peer=channel,
                reason=reason,
                message=message
            ))
            print(f"[{account['phone']}] Telethon report #{i+1} sent: {result}")
            await asyncio.sleep(random.uniform(1, 2))
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
            await asyncio.sleep(random.uniform(3, 7))
        print(f"Cycle {cycle} complete. Waiting for next round...\n")
        await asyncio.sleep(random.randint(30, 60))
        cycle += 1

if __name__ == "__main__":
    asyncio.run(mass_report())
