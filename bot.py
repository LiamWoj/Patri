import os
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands

# --- Load .env token ---
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("Discord token niet gevonden!")

# --- Bot setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.voice_states = True  # Belangrijk voor voice events

bot = commands.Bot(command_prefix="!", intents=intents)

TRIGGERS = {
    "patri": "EY MAMA MIA",
    "lucht": "MANIPULATIE VAN DE WEER!",
    "wk": "TIJD VOOR HET WK OHHHH WAT SPANNEND!",
    "dujardin": "HEY DUJARDIN!",
}

# --- Event: Reageer op berichten ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    for word, response in TRIGGERS.items():
        if word in content:
            await message.channel.send(response)
            break

    await bot.process_commands(message)

# --- Voice join voor specifieke gebruiker ---
TARGET_USER_ID = 1097126388236030083  # Vervang dit door de Discord ID van de persoon
MP3_FILE = r"C:\Users\Liam Wojciechowski\mijn-discord-bot\voorbeeld.mp3"  # pad naar MP3
FFMPEG_PATH = r"C:\Users\Liam Wojciechowski\ffmpeg-2025-12-01-git-7043522fe0-full_build\ffmpeg-2025-12-01-git-7043522fe0-full_build\bin\ffmpeg.exe"

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id != TARGET_USER_ID:
        return

    if before.channel is None and after.channel is not None:
        channel = after.channel

        # Check of bot al verbonden is
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client is None:
            voice_client = await channel.connect()

        print(f"Speelt MP3 af: {MP3_FILE}")
        audio_source = discord.FFmpegPCMAudio(source=MP3_FILE, executable=FFMPEG_PATH)
        if not voice_client.is_playing():
            voice_client.play(audio_source)

        # Wacht tot afspelen klaar is en disconnect
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

# --- Commands: join / leave ---
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("Je moet eerst in een voice channel zitten!")
        return

    channel = ctx.author.voice.channel

    # Check of bot al verbonden is
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await channel.connect()
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("Ik ben al verbonden in een voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Bye! 👋")
    else:
        await ctx.send("Ik zit nergens in een voice channel.")

# --- Run bot ---
bot.run(TOKEN)