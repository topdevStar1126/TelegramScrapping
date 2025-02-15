from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os
from datetime import datetime

# Config
class Config:
    BOT_TOKEN = "8151983253:AAH3kJebKs89moyrmzFv4JW09kSm4hbPhFQ"
    CHANNEL_ID = -1001717037581
    API_ID = 24876084
    API_HASH = "a1934a433c25897914d5c23803a38444"


# Session string (replace with your session string)
session = StringSession('1BSABCyjyP_AFAAAAAAAAAAoBu2RXpXVswqDYtlZz1ltquOOEnkjGnbOiQBiqDEmULPUHxsdlcH5yI7r6wPwyO8SUp5rwJ61n8Y85kgXnZIKr9WwFyTCj5GFHvf_NX6FLCX6SofagfRZ1w54B0EF-L-ql70690fsFZl0wkwiEWmUcu4_fnoelVtXDOCNkhWkL5IQrp-b3RDju3CaW9T1OQwrxzE63kb06ahpqh2l7MvW_jaCdAk4IEzHIr7yKxGmfHW15z21o89NuIGseSmSN32wNIcZ_YfxJXAad1my0leYKIuLTOqiBP4-9NR6qlqKbn59FM94wp7S38QyTqVGJ3mIa7wOrviFudmYP_m48lmdvOlQ=')

async def main():
    print('Initializing...')
    client = TelegramClient(
        session,
        Config.API_ID,
        Config.API_HASH,
        connection_retries=5,
        use_ipv6=True,
        timeout=30
    )

    @client.on(events.NewMessage(chats=[Config.CHANNEL_ID]))
    async def handler(event):
        message = event.message
        print('New message:', {
            'id': message.id,
            'date': datetime.fromtimestamp(message.date.timestamp()),
            'text': message.text
        })

    try:
        print('Connecting...')
        await client.connect()
        
        print('Starting authentication...')
        if not await client.is_user_authorized():
            # Phone number authentication
            phone = input('Phone number (include country code, e.g., +1234567890): ')
            print('Sending code to:', phone)
            await client.send_code_request(phone)
            
            # Code verification
            print('Waiting for code input...')
            code = input('Enter the code you received: ')
            await client.sign_in(phone, code)
            
            if await client.is_user_authorized():
                print('Authentication successful!')
                print('\nYour session string (save this):', client.session.save())

        print('Listening for new messages...')
        await client.run_until_disconnected()

    except Exception as error:
        print('Detailed error:', str(error))
        raise error

    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 
