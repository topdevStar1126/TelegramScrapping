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
session = StringSession('1BCABBnwE6PAEAAAAAAAAAAoBuw3TWMp_6Bg2FUdx9gZOR80ltWpc_gs29MqVcl7SyiV5Tgy66vINYEokf1YAnfV_7qXCmwbZAQDp7-GXlEJI-i-vL6D4CmNfhGlvyCEflHXULmpyCS3YyjG6wxoIDL1jVWy4G6UOFYGIlMuslJENj2obtrUIUDzvO6ME22c_9xbNMWkRLDH4n7usA9ygWEXKg57BkeGV90zxPWU4rCJ4zSFfF5WdhG6fCMxnOUs_AoOMCNQsuDC8-7wuuGB_WkwoAv9JXAJQ5MYlNdFrfvdGHjmYc8f761cIUWG_NA-HqEUeFguCKHSMJJJ5ZhUJaXU4coXOPcojNQGHtOOMsBgzzlA=')

def parse_trading_signal(message: str):
    try:
        # Split message into lines and remove empty lines
        lines = [line.strip() for line in message.split('\n') if line.strip()]
        
        # Validate basic structure
        if len(lines) < 6:  # At least header, entry, and 4 TP levels
            return None
            
        # Parse header
        header = lines[0]
        if not header.startswith('🔥'):
            return None
            
        # Extract symbol and position type
        symbol_info = header.split(' ')[1]  # "#AUCTION/USDT"
        symbol = symbol_info.replace('#', '')
        position_type = 'LONG' if 'Long📈' in header else 'SHORT' if 'Short📉' in header else None
        leverage = header.split('x')[1].strip('🔥 )')  # "20"
        
        # Extract entry price
        entry_line = lines[1]
        entry_price = float(entry_line.split('-')[1].strip())
        
        # Extract take profit levels
        tp_levels = []
        for line in lines[3:7]:  # 4 TP levels
            price = float(line.split(' ')[1])
            percentage = int(line.split('(')[1].split('%')[0])
            tp_levels.append({
                'price': price,
                'percentage': percentage
            })
        
        return {
            'symbol': symbol,
            'position_type': position_type,
            'leverage': int(leverage),
            'entry_price': entry_price,
            'take_profit_levels': tp_levels
        }
        
    except Exception as e:
        print(f"Error parsing message: {e}")
        return None

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
        signal = parse_trading_signal(message.text)
        
        if signal:
            # Format the extracted information
            formatted_message = (
                f"🎯 New Trading Signal\n\n"
                f"Symbol: {signal['symbol']}\n"
                f"Position: {signal['position_type']}\n"
                f"Leverage: {signal['leverage']}x\n"
                f"Entry Price: {signal['entry_price']}\n\n"
                f"Take Profit Levels:\n"
            )
            
            for i, tp in enumerate(signal['take_profit_levels'], 1):
                formatted_message += f"TP{i}: {tp['price']} ({tp['percentage']}%)\n"
            
            # Send formatted message to your channel
            try:
                await client.send_message(-1002451169737, formatted_message)
                print("Signal processed and forwarded successfully!")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("Message received but not a valid trading signal")

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
        
        await client.send_message(-1002451169737, "Your message here")
        print("Message sent successfully!");

        print('Listening for new messages...')
        await client.run_until_disconnected()

    except Exception as error:
        print('Detailed error:', str(error))
        raise error

    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 
