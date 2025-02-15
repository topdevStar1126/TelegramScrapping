from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os
from datetime import datetime

# Config
class Config:
    BOT_TOKEN = "8151983253:AAH3kJebKs89moyrmzFv4JW09kSm4hbPhFQ"
    CHANNEL_ID = -1002418565988
    API_ID = 24876084
    API_HASH = "a1934a433c25897914d5c23803a38444"


# Session string (replace with your session string)
session = StringSession('1BCABBnwE6PAEAAAAAAAAAAoBu2Pf00bu_7g6kFy7F_QWJXxP-s8l666K3gqyeeuW2nj2AWq4CtjANAHtNjKf6c9sajkhmiS5YlXK9A7VIqzgMrxfcANNktR8JqkdvRKJtFv5kt_1K4xIU3kjXaG7nOqljlejN8HrqsiWRZiOATAWItIgRwmu8eDRFvafZGghdCSl3ExpFTcea1jzWML4KZylM54qWV342b22txniRdkKJe441yQ5yvKMQ-AxK_yQ9VU3iY_tRP8ZKa65RkwTXxUZ0E0k4R2JjnqzrjfhOlVQeFVmUZqa7Gwgpnjo88Y_UCe05OP1IWG0RyrMfSUgPop0k1oKFb1ISBfTrXwhXA7Q6Vs=')

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
