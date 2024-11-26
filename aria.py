import discord
from discord.ext import commands, tasks
import requests

bot = commands.Bot(command_prefix='!')

# Dictionary to store server-specific settings
server_settings = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    check_twitch_live.start()

@bot.command()
async def set(ctx, service: str, twitch_channel: str, announcement_channel: discord.TextChannel, role: str):
    if service.lower() == 'twitch':
        server_settings[ctx.guild.id] = {
            'twitch_channel': twitch_channel,
            'announcement_channel': announcement_channel.id,
            'role': role
        }
        await ctx.send(f'Twitch channel set to {twitch_channel} and announcements will be made in {announcement_channel.mention} for {role}.')

@tasks.loop(minutes=1)
async def check_twitch_live():
    for guild_id, settings in server_settings.items():
        twitch_channel = settings['twitch_channel']
        announcement_channel_id = settings['announcement_channel']
        role = settings['role']
        
        # Check if the Twitch channel is live
        if is_twitch_live(twitch_channel):
            guild = bot.get_guild(guild_id)
            announcement_channel = guild.get_channel(announcement_channel_id)
            await announcement_channel.send(f'@{role} {twitch_channel} is live! https://twitch.tv/{twitch_channel}')

def is_twitch_live(twitch_channel):
    # Replace 'your_client_id' and 'your_access_token' with your actual Twitch API credentials
    headers = {
        'Client-ID': 'your_client_id',
        'Authorization': 'Bearer your_access_token'
    }
    response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={twitch_channel}', headers=headers)
    data = response.json()
    return len(data['data']) > 0

# ...existing code...

bot.run('your_discord_bot_token')