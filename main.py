from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import socket

# Loading Token from .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

# Function to ping a host and port
def ping(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            return True
    except socket.error:
        return False

# Handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    if user_message.startswith('?dcsstatus'):
        # Define the server IP and port
        server_ip = '81.130.215.226'  # Server IP address
        server_port = 10308  #DCS server port

        if ping(server_ip, server_port):
            await message.channel.send("The White Martian DCS Server is online.")
        else:
            await message.channel.send("The White Martian DCS Server is currently offline. Please join this Discord server: discord.gg/Aup5Knd if the problem continues.")

# Handling the discord bot startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Main Entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()