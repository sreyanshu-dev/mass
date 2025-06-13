from telethon import TelegramClient, functions, types
import asyncio
import os
import random
import time

ACCOUNTS = [
    {"phone": "+917470479257", "api_id": 29400566, "api_hash": "8fd30dc496aea7c14cf675f59b74ec6f"},
    {"phone": "+919343771145", "api_id": 29400566, "api_hash": "8fd30dc496aea7c14cf675f59b74ec6f"}
]

TARGET_CHANNEL = "The_Grabbers"
REPORT_REASONS = [
    types.InputReportReasonCopyright(),
    types.InputReportReasonSpam(),
    types.InputReportReasonViolence(),
    types.InputReportReasonChildAbuse(),
    types.InputReportReasonOther()
]
REPORT_MESSAGES = [
    "Distributing pirated movies: DMCA Case #%0d" % random.randint(100000,999999),
    "Child abuse content detected! Urgent action needed!",
    "Selling illegal drugs through this channel",
    "Terrorism promotion content found @%0d" % random.randint(1000,9999),
    "Repeated copyright violations - Legal action pending"
]
SESSION_DIR = "sessions_aggressive"
os.makedirs(SESSION_DIR, exist_ok=True)

async def aggressive_report(account):
    session_file = f"{SESSION_DIR}/{account['phone']}"
    client = TelegramClient(session_file, account['api_id'], account['api_hash'])
    
    try:
        await client.start()
        if not await client.is_user_authorized():
            print(f"[{account['phone']}] Login failed! Run manually once.")
            return False
            
        channel = await client.get_entity(TARGET_CHANNEL)
        
        while True:  # Infinite loop for non-stop reporting
            try:
                # Send rapid burst of reports
                for _ in range(random.randint(80, 120)):  # 80-120 reports per burst
                    await client(functions.account.ReportPeerRequest(
                        peer=channel,
                        reason=random.choice(REPORT_REASONS),
                        message=random.choice(REPORT_MESSAGES)
                    ))
                    await asyncio.sleep(random.uniform(0.1, 0.5))  # Faster delay
                
                # Random profile changes to avoid detection
                await client(functions.account.UpdateProfileRequest(
                    first_name=f"User{random.randint(1000,9999)}",
                    last_name=f"Bot{random.randint(1,9)}"
                ))
                
            except Exception as e:
                print(f"[{account['phone']}] Critical error: {e}")
                break  # Exit loop on major errors
                
    finally:
        await client.disconnect()

async def mass_attack():
    tasks = []
    for account in ACCOUNTS:
        tasks.append(aggressive_report(account))
        await asyncio.sleep(1)  # Staggered start
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    while True:  # Auto-restart if all accounts fail
        try:
            asyncio.run(mass_attack())
        except:
            print("All accounts exhausted! Restarting in 60 seconds...")
            time.time.sleep(60)
