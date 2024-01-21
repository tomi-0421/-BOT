import discord
import asyncio
from discord.ext import commands, tasks
import datetime

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_channel.start()

@tasks.loop(minutes=1)
async def update_channel():
    guild = bot.get_guild(YOUR_GUILD_ID)  # サーバーIDを指定
    category = discord.utils.get(guild.categories, name='Time Channels')  # カテゴリー名を指定

    if category is None:
        # カテゴリーが存在しない場合は作成
        category = await guild.create_category('Time Channels')

    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    channel_name = f'time_{formatted_time}'  # チャンネル名に現在の時間を使用

    # すでに同じ名前のチャンネルが存在する場合はスキップ
    if discord.utils.get(category.channels, name=channel_name) is not None:
        return

    new_channel = await category.create_text_channel(channel_name)
    await new_channel.send(f'現在の時間: {formatted_time}')

@bot.command()
async def stop(ctx):
    update_channel.stop()
    await ctx.send('毎分時間を更新するチャンネルの作成が終了しました。')

bot.run('YOUR_BOT_TOKEN')
