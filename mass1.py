from telethon import TelegramClient, functions, types
import asyncio
import os
import random
import time

ACCOUNTS = [
    {"phone": "+1234567890", "api_id": 12345, "api_hash": "abcdef1234567890abcdef"},
    {"phone": "+0987654321", "api_id": 67890, "api_hash": "fedcba0987654321fedcba"}
]

TARGET_CHANNEL = "target_channel_username"
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
SESSION_DIR = "sessions"
os.makedirs(SESSION_DIR, exist_ok=True)

async def report_channel(account):
    session_file = f"{SESSION_DIR}/{account['phone']}"
    client = TelegramClient(session_file, account['api_id'], account['api_hash'])
    try:
        await client.start()
        if not await client.is_user_authorized():
            print(f"[{account['phone']}] Login required. Skipping...")
            return False
        channel = await client.get_entity(TARGET_CHANNEL)
        reason = random.choice(REPORT_REASONS)
        message = random.choice(REPORT_MESSAGES)
        for i in range(random.randint(2, 5)):  # Multiple reports per account per cycle
            result = await client(functions.account.ReportPeerRequest(
                peer=channel,
                reason=reason,
                message=message
            ))
            print(f"[{account['phone']}] Report #{i+1} sent: {result}")
            await asyncio.sleep(random.uniform(2, 7))  # Random delay between reports
        return True
    except Exception as e:
        print(f"[{account['phone']}] Error: {e}")
        return False
    finally:
        await client.disconnect()

async def mass_report():
    cycle = 1
    while True:
        print(f"\n=== Reporting Cycle {cycle} ===")
        tasks = []
        for account in ACCOUNTS:
            tasks.append(report_channel(account))
            await asyncio.sleep(random.uniform(5, 15))  # Random delay between accounts
        await asyncio.gather(*tasks)
        print(f"Cycle {cycle} complete. Waiting before next round...\n")
        await asyncio.sleep(random.randint(120, 300))  # Wait 2-5 min between cycles
        cycle += 1

if __name__ == "__main__":
    asyncio.run(mass_report())
