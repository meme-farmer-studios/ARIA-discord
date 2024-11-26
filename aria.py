import discord
import json
import os
import asyncio
from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch

# Load or create the settings file
settings_file = 'settings.json'
if os.path.exists(settings_file):
    with open(settings_file, 'r') as f:
        settings = json.load(f)
else:
    settings = {}

# Prompt for missing credentials
if 'TWITCH_CLIENT_ID' not in settings or 'TWITCH_CLIENT_SECRET' not in settings or 'DISCORD_TOKEN' not in settings:
    settings['TWITCH_CLIENT_ID'] = input('Enter your Twitch Client ID: ')
    settings['TWITCH_CLIENT_SECRET'] = input('Enter your Twitch Client Secret: ')
    settings['DISCORD_TOKEN'] = input('Enter your Discord Bot Token: ')
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)

# Twitch API credentials
TWITCH_CLIENT_ID = settings['TWITCH_CLIENT_ID']
TWITCH_CLIENT_SECRET = settings['TWITCH_CLIENT_SECRET']
DISCORD_TOKEN = settings['DISCORD_TOKEN']

# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix='ARIA, ', intents=intents)

async def setup():
    global twitch
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
    await bot.start(DISCORD_TOKEN)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_live_channels.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'Invalid command. Please use a valid command.')
    elif not isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'An error occurred: {str(error)}')

@bot.command()
async def set(ctx, service: str, twitch_channel: str, service_channel: discord.TextChannel, role_name: str):
    if service.lower() == 'twitch':
        # Check if the Twitch channel exists
        user_info = [user async for user in twitch.get_users(logins=[twitch_channel])]
        if not user_info:
            await ctx.send(f'Twitch channel {twitch_channel} not found.')
            return
        
        # Handle the special case for @everyone
        if role_name.lower() == 'everyone':
            role = discord.utils.get(ctx.guild.roles, name='@everyone')
            role_display_name = 'everyone'
        else:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            role_display_name = role.name if role else role_name
        
        if not role:
            await ctx.send(f'Role {role_name} not found.')
            return
        
        settings[str(ctx.guild.id)] = {
            'twitch_channel': twitch_channel,
            'service_channel': service_channel.id,
            'role': role.id
        }
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
        await ctx.send(f'Settings saved for {twitch_channel} in {service_channel.mention} with role {role_display_name}')

@set.error
async def set_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing parameter: {error.param}. Usage: ARIA, set [service] [twitch_channel] [text_channel] [role]. Please note that roles are case-sensitive.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'Invalid argument. Usage: ARIA, set [service] [twitch_channel] [text_channel] [role]. Please note that roles are case-sensitive.')
    else:
        await ctx.send(f'An error occurred: {str(error)}')

@tasks.loop(minutes=1)
async def check_live_channels():
    for guild_id, setting in settings.items():
        if not isinstance(setting, dict):
            continue
        twitch_channel = setting['twitch_channel']
        service_channel_id = setting['service_channel']
        role_id = setting['role']
        
        # Check if the Twitch channel is live
        user_info = [user async for user in twitch.get_users(logins=[twitch_channel])]
        if user_info:
            user_id = user_info[0]['id']
            streams = [stream async for stream in twitch.get_streams(user_id=user_id)]
            if streams:
                channel = bot.get_channel(service_channel_id)
                role = discord.utils.get(channel.guild.roles, id=role_id)
                await channel.send(f'{role.mention} {twitch_channel} is live! https://twitch.tv/{twitch_channel}')

@bot.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    with open('aria_signal.txt', 'w') as f:
        f.write('shutdown')
    await bot.close()

@bot.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.send("Restarting...")
    with open('aria_signal.txt', 'w') as f:
        f.write('restart')
    await bot.close()

@bot.command()
@commands.has_permissions(administrator=True)
async def update(ctx):
    await ctx.send("Updating...")
    with open('aria_signal.txt', 'w') as f:
        f.write('update')
    await bot.close()

# Run the setup function
asyncio.run(setup())